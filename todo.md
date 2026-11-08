# Slide TODOs


## Slide 6:

- [x] Remove OTLP from langsmith, it's SDK-based

## Slide 9

- [x] Find a realistic problem caused by broken context and talk through it.
- [x] Make it relatable to someone who is not deep into tracing.

## Slide 10

- [x] Merge the duplicate wish list into the Wish/OpenTelemetry table, keeping "If I had a magic wand".
- [x] Narrative context: slides 1-9 focus on problems; slide 10 connects the wishes to solutions, revealed in the table.
- [x] Consider a transition slide between the problems and solutions.

## Slide 17

- [x] Replace the donation slide with a six-milestone 2026 project timeline.
- [x] Merge slide 24 into it (adoption slide removed).
- [x] Include the AAIF observability working group in the May milestone.
- [x] Mark the start of GenAI semconv stabilization in September, using tracking issue #511.
- [x] Put distinct updates on separate lines with consistent text size; list native Anthropic tracing first in October-November and omit "shared".
- [x] Use the [expanded 2026 research](kubecon-talk-research.md#2026-timeline-beyond-python-and-javascript) for the past milestones, with sources and date qualifications in the slide notes.
- [x] Continue the timeline into the future in the closing slides.
- [x] Visually check timeline spacing and text fit in the browser; computer-use permissions blocked the preview.

## Slide 18

- [x] Trim the Python example to the inference call, usage mapping, and return.
- [x] make slide look better: split into a text slide ("How we build instrumentations") and a code slide ("A thin adapter").

## Slide 19

- [x] Expand the numbers / text to include Java, Go, eBPF, Ruby, and other GenAI instrumentation projects.

## Slide 22

- [x] Column 3: check the report.
- [x] Change "compare JSON" to "View report".
- [x] Consider adding a slide on Weaver. Drop it later if there is not enough time.

## Slide 23

- [x] Consider showing the [conformance report](https://open-telemetry.github.io/semantic-conventions-conformance/#/signals/span%3Agen_ai.client.inference?q=anthropic&level=scored) live.
- [x] Display only the report's base URL verbatim, without the snapshot caption, so people can capture it in a photo.
- [x] Use GitHub icons and `owner/repo` link labels throughout the deck. Slide 27 uses shorter repo-only labels; Slack uses its channel name and a colorful icon.

## Slides 24/25/26

- [x] Resolve overlap: removed slide 24 (community adoption); the timeline on slide 17 covers it. Slides 25/26 cover the future.
- [x] Consider two future timeline slides: near future and long term. Merged into one roadmap slide instead.
- [x] Near future: depth and detail, RC by EOY, and the next features to stabilize.
- [x] Long term: breadth and 2027 areas, including security / CoSAI, AAIF collaboration, evaluations, guardrails / safety, harnesses, and trajectories. CoSAI not named on the slide.
- [x] Invite the audience to come shape this work with us.

## Slide 27

- [x] Use "Let's build it together" as the title; remove introductory text and bullets.
- [x] Add Slack, conventions, conformance, and Python/JS/Java/Go/Ruby/eBPF repo links. JS links to GenAI utilities; omit .NET.
- [x] Put Slack on its own row in an equal-width card, with conventions and conformance side by side below.
- [x] Group language repos under "OpenTelemetry Instrumentations" in equal-sized, multicolored tiles with larger text.

## Slide 28

- [x] Move "Thank you" to a separate final slide.
- [x] Keep the KubeCon background; remove logos, names, and the feedback caption.
- [x] Center the 440px feedback QR code horizontally and vertically.
- [x] Center "Thank you!" horizontally at 40px, keeping the standard heading's vertical position.
