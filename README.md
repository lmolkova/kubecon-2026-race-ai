# The Race to Standardize AI Observability

Talk materials by **Liudmila Molkova (Google)** and **Trask Stalnaker (Microsoft)**.

[Official session](https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/program/schedule/?id=1246166): KubeCon + CloudNativeCon North America 2026, November 12, 13:50-14:20 MST, Salt Lake City. Observability track, any level.

The repository name is `kubecon-2027-race-ai`; the linked session is on the 2026 schedule.

## Start here

- **[Slides](slides/kubecon-genai.md)**: the current Markdown deck, with screenshots, charts, SQL examples, and TODOs.
- [Slide assets and sources](slides/README.md).
- [Demo](demos/kubecon-genai/README.md): one application, mixed instrumentation and OTel variants.
- [Research](kubecon-talk-research.md): adoption evidence, contributor statistics, and references.
- [Outline](kubecon-talk-outline.md): planning material; the slides reflect the latest edits.

The talk follows a team trying to build dashboards from fragmented GenAI telemetry, then shows how semantic conventions, shared instrumentation utilities, and conformance testing help.

## Run the demo

Requires Docker with Compose and Python 3 for the telemetry inspection script. Model responses come from a local mock server; no model-provider credentials or cloud accounts are needed.

```sh
cd demos/kubecon-genai
docker compose up --build -d
curl --fail-with-body http://localhost:8000/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
python3 inspect_demo.py
```

Open [Aspire](http://localhost:18888) for the mixed-instrumentation demo.

For the parallel OTel instrumentation demo:

```sh
docker compose -f compose.otel.yaml up --build -d
curl --fail-with-body http://localhost:8010/run \
  -H 'Content-Type: application/json' -d '{"scenario":"mixed"}'
ASPIRE_URL=http://localhost:18889 python3 inspect_demo.py
```

Open [Aspire for OTel](http://localhost:18889). Both stacks can run together. See the [demo README](demos/kubecon-genai/README.md) for scenarios, verification, and known behavior.

Stop them with:

```sh
docker compose down
docker compose -f compose.otel.yaml down
```

## Editing the slides

Edit `slides/kubecon-genai.md`. Slides use `---` separators, Mermaid diagrams, fenced code, and HTML layouts. Use a renderer that supports these features. Screenshots and charts are committed under `slides/assets/`, so viewing the deck does not require running the demo. TODOs remain visible; speaker notes have been removed.

## License

[MIT](LICENSE) for the original talk materials and demo code. Referenced projects, dependencies, and third-party screenshots retain their respective licenses and trademarks.
