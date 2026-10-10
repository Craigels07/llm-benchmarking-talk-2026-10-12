# LLM benchmark explorer

A single-page chart for comparing OpenAI and Anthropic models on intelligence, cost, output speed and latency, using
data from [Artificial Analysis](https://artificialanalysis.ai/). No framework and no build step: a Python script fetches
the data, and `index.html` draws it with [Plotly.js](https://plotly.com/javascript/).

## What it does

- **Pick 2–4 metrics:** Intelligence Index, price (blended $ per 1M tokens), output speed (tokens/s) and latency (time to
  first answer token). Two metrics give a 2D scatter, three a 3D scatter, and a fourth sets the marker size.
- **Intelligence is always vertical:** the y axis in 2D, the z axis in 3D.
- **Rotate the 3D chart with the mouse.** It stays upright, so dragging cannot flip it over. Buttons jump to a default
  3D view or a side-on view of each pair of axes.
- **Filter by provider or model:** provider checkboxes, plus a searchable model list with select all/none.
- **Trend lines:** one best-fit line per provider with at least three plotted models, solid across its models and dashed for a projection past them.
  It is a straight-line extension, not a forecast.
- **Log scale** per axis for price, speed and latency. **Light and dark themes**, which follow your system setting and
  remember your choice.

## Setup

1. Get a free API key from [Artificial Analysis](https://artificialanalysis.ai/) and put it in a `.env` file in the repo
   root (it is gitignored):

   ```text
   AA_API_KEY=your-key-here
   ```

2. Fetch the data (Python 3, standard library only):

   ```sh
   python fetch_data.py          # OpenAI and Anthropic only (edit PROVIDERS at the top of the file)
   python fetch_data.py --all    # every provider
   ```

   This writes `data/models.json`, which the page reads. The key is only used by this script, never by the page. The
   free tier allows 1,000 requests per day.

3. Serve the folder and open <http://localhost:8000> (not `0.0.0.0:8000`, which Windows browsers cannot open):

   ```sh
   python -m http.server
   ```

## Notes

- `data/` is gitignored. The Artificial Analysis
  [Data Platform Terms](https://artificialanalysiscdn.com/legal/ProDataPlatformTerms.pdf) do not allow publishing raw
  data files, so each user fetches their own copy.
- Models missing a value for any active metric are left out of the chart and counted. The API reports 0 for output
  price, speed and latency when it has no value (for example ChatGPT-only or retired models), so those zeros are
  treated as missing.
- **Price is not cost per task.** The price axis is the list price per 1M tokens, blended 3 parts input to 1 part
  output. Models that write more tokens cost more per task than their price suggests: per Artificial Analysis, Claude
  Opus 5.5 ($4/$20 per 1M) costs about $5.98 per Intelligence Index task, while GPT-6 Astra ($10/$50 per 1M) costs
  about $3.26.
- Per-task metrics (cost, time and output tokens per task) are not available in the free API, so they are not shown.

## Files

| File | Purpose |
| --- | --- |
| `fetch_data.py` | Calls the Artificial Analysis API and writes `data/models.json` |
| `index.html` | The chart page: controls, filters, themes, trend lines |

## Attribution

Data: [Artificial Analysis](https://artificialanalysis.ai/). Attribution is required by their API terms.
