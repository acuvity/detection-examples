import argparse
import json
import os
import re
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path

import jinja2
import requests

template = """
{% if content %}
Content:

```{{ modalities[0].type }}
{{ content.decode("utf-8") }}
```
{%- else %}

{%- if modalities[0].group == "image" -%}
![{{ file_name }}](<assets/{{ file_path }}>)
{%- else -%}
[{{ file_name }}](<assets/{{ file_path }}>)
{%- endif -%}
{%- endif -%}

{%- if modalities %}

Modality:
{%- for modality in modalities %}
  - *{{ modality.group }}/{{ modality.type }}*
{%- endfor %}
{% endif -%}

{%- if categories %}
Category:
{%- for category in categories %}
  - *{{ category.group }}/{{ category.type }}*
{%- endfor %}
{% endif -%}

{%- if intent %}
Intent:
{%- for name, score in intent|dictsort %}
 - *{{ name }}: {{ score }}*
{%- endfor %}
{% endif -%}

{%- if languages %}
Languages:
{%- for name, score in languages|dictsort %}
 - *{{ name }}: {{ score }}*
{%- endfor %}
{% endif -%}

{%- if exploits %}
Exploits:
{%- for name, score in exploits|dictsort %}
 - *{{ name }}: {{ score }}*
{%- endfor %}
{% endif -%}

{%- if malcontents %}
Malcontents:
{%- for name, score in malcontents|dictsort %}
 - *{{ name }}: {{ score }}*
{%- endfor %}
{% endif -%}

{%- if secrets %}
Secrets:
{%- for name, values in secrets|dictsort %}
 - *{{ name }}*:
{%- for value in values %}
{%- if value.end != 0 %}
   - start: {{ value.start }}, end: {{ value.end }}, score: {{ value.score }} (`{{content[value.start:value.end].decode("utf-8")}}`)
{%- else %}
   - score: {{ value.score }}
{%- endif -%}
{% endfor %}
{% endfor %}
{% endif -%}

{%- if piis %}
PIIs:
{%- for name, values in piis|dictsort %}
 - *{{ name }}*:
{%- for value in values %}
{%- if value.end and value.end != 0 %}
   - start: {{ value.start }}, end: {{ value.end }}, score: {{ value.score }} (`{{content[value.start:value.end].decode("utf-8")}}`)
{%- else %}
   - score: {{ value.score }}
{%- endif -%}
{% endfor %}
{% endfor %}
{% endif -%}

{%- if keywords %}
Keywords:
{%- for name, values in keywords|dictsort %}
 - *{{ name }}*:
{%- for value in values %}
{%- if value.end != 0 %}
   - start: {{ value.start }}, end: {{ value.end }}, score: {{ value.score }} (`{{content[value.start:value.end].decode("utf-8")}}`)
{%- else %}
   - score: {{ value.score }}
{%- endif -%}
{% endfor %}
{% endfor %}
{% endif -%}

{%- if cdt %}
Custom Data types:
{%- for name, values in cdt|dictsort %}
 - *{{ name }}*:
{%- for value in values %}
{%- if value.end != 0 %}
   - start: {{ value.start }}, end: {{ value.end }}, score: {{ value.score }} (`{{content[value.start:value.end].decode("utf-8")}}`)
{%- else %}
   - score: {{ value.score }}
{%- endif -%}
{% endfor %}
{% endfor %}
{% endif -%}

{%- if topics %}
Topics:
{%- for name, score in topics|dictsort %}
 - *{{ name }}: {{ score }}*
{%- endfor %}
{%- endif %}

"""


def sort_by_name(data):
    s = data["file_name"]
    if "_" in s:
        parts = s.split("_", 1)
        if len(parts) > 1:
            try:
                return (0, int(parts[1]))
            except ValueError:
                pass
    match = re.search(r"\d+", s)
    if match:
        return (0, int(match.group()))
    return (1, s.lower())


def send_request(url, token, namespace, file_path):
    with open(file_path, "rb") as f:
        data = {"data": (os.path.basename(file_path), BytesIO(f.read()), "text/plain")}

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "X-Namespace": namespace},
        files=data,
        data={"request": "{}"},
    )
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    result = json.loads(response.text)
    result["file_path"] = Path(file_path).as_posix()
    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--assets",
        type=str,
        help="The path to assets to test.",
        default="assets/",
    )
    parser.add_argument(
        "--workers",
        type=int,
        help="The number of concurent workers.",
        default="5",
    )

    args = parser.parse_args()

    token = os.environ.get("ACUVITY_TOKEN")
    namespace = os.environ.get("ACUVITY_NAMESPACE")
    host = os.environ.get("ACUVITY_API_URL")

    if not host:
        raise Exception("No host provided in ACUVITY_API_URL")
    if not namespace:
        raise Exception("No namespace provided in ACUVITY_NAMESPACE")
    if not token:
        raise Exception("No token provided in ACUVITY_TOKEN")

    responses = []
    futures = []
    file_list = []

    path = Path(args.assets)
    if path.is_dir():
        files = path.rglob("*")
    else:
        files = [path]
    for file_path in files:
        if file_path.is_file():
            file_list.append(file_path)

    if not file_list:
        raise Exception("no files found for %s", args.assets)

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(
                send_request,
                host,
                token,
                namespace,
                file_path,
            )
            for file_path in file_list
        ]

    with tempfile.TemporaryDirectory() as results:
        for future in as_completed(futures):
            result = future.result()
            file_path = result["file_path"]
            output = f"{os.path.basename(file_path)}.json"
            with open(os.path.join(results, output), "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

        file_list = []

        path = Path(results)
        if path.is_dir():
            files = path.rglob("*.json")
        else:
            files = [path]
        for file_path in files:
            if file_path.is_file():
                file_list.append(file_path)

        if not file_list:
            raise Exception("no files found for %s", args.assets)

        t = jinja2.Template(template)
        groups = {}
        for f in file_list:
            with open(f, "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(data["file_path"], "rb") as d:
                file_content = d.read()

            data["file_path"] = data["file_path"].replace(".json", "")
            data["file_name"] = os.path.basename(data["file_path"])
            subgroup = os.path.basename(os.path.dirname(data["file_path"]))
            group = os.path.basename(
                os.path.dirname(os.path.dirname(data["file_path"]))
            )
            data["file_path"] = os.path.join(group, subgroup, data["file_name"])
            try:
                _ = file_content.decode("utf-8")
                data["content"] = file_content
            except UnicodeDecodeError:
                pass

            groups.setdefault(group, {}).setdefault(subgroup, []).append(data)

        with open("README.md", "w") as f:
            # Write header and image
            f.write(
                '<img src="https://raw.githubusercontent.com/acuvity/detection-examples/refs/heads/master/icons/acuvity.png" width="100" height="100">\n\n'
            )
            f.write("# Acuvity analyses report\n\n")
            f.write(
                "The following sections contain examples for different modalities with the corresponding expected outputs.\n\n"
            )

            f.write("## Table of Content\n\n")
            for group in sorted(groups):
                group_anchor = group.lower()
                f.write(f"- [{group.capitalize()}](#{group_anchor})\n")
                for subgroup in sorted(groups[group]):
                    subgroup_anchor = f"{group.lower()}-{subgroup.lower()}"
                    f.write(f"  - [{subgroup.capitalize()}](#{subgroup_anchor})\n")
            f.write("\n\n")

            for group in sorted(groups):
                group_anchor = group.lower()
                f.write(f'# {group.capitalize()} <a name="{group_anchor}"></a>\n\n')
                for subgroup in sorted(groups[group]):
                    subgroup_anchor = f"{group.lower()}-{subgroup.lower()}"
                    f.write(
                        f'## {subgroup.capitalize()} <a name="{subgroup_anchor}"></a>\n\n'
                    )
                    for data in sorted(groups[group][subgroup], key=sort_by_name):
                        name = data["file_name"]
                        data_anchor = f"{group.lower()}-{subgroup.lower()}-{name.lower().replace(' ', '-').replace('.', '')}"
                        f.write(
                            f'### [{name.capitalize()}](<assets/{data["file_path"]}>) <a name="{data_anchor}"></a>\n\n'
                        )
                        f.write(t.render(**data))
                        f.write("\n\n")
