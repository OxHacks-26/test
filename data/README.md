# Sea turtle data handoff

`species.json` contains all seven living species, display colours, geographic summaries,
published depth examples, facts, regional nesting months and citation IDs.
`sources.json` resolves those IDs to source titles, links and the claims they support.

**`migrations.geojson` is stub data, not downloaded telemetry.** It contains seven
hand-authored LineStrings with twelve invented monthly positions each. The 2025 dates
are arbitrary animation timestamps. Show an **Illustrative route — not observed tracking**
label wherever these routes appear. They are suitable for developing the month slider,
not for predicting turtle positions or reporting conservation results.

## Data contract

- Join `species[].id` to `features[].properties.species_id`.
- GeoJSON positions are `[longitude, latitude]` in WGS84, never `[latitude, longitude]`.
- Route `coordinates[i]`, `dates[i]`, `months[i]` and `depth_m[i]` describe the same point.
- Months are integers 1–12. Dates are ISO 8601 UTC strings.
- `depth_m` values are null: no measured depths were obtained for route positions.
- Species depth values use metres positive down. Read `depth_context` alongside every
  range. They mix explicitly described study statistics and are not directly comparable
  species-wide distributions. `study_max_dive_m` is a cited study maximum, not a record
  for the species. Do not assign a species range to an observed turtle position.
- Nesting calendars apply only to the named region, not all populations. They are not
  evidence for the invented route dates. In particular the leatherback depth example
  comes from Gabon, while its regional nesting calendar describes Queensland.
- Colours and demo geometry are project choices; source citations do not substantiate
  invented coordinates or exact movements. No satellite-tag identifiers are fabricated.

For a cumulative month trail, select positions through the slider month. At January
there is only one point: render a Point marker, and only construct a LineString once
there are at least two positions. Do not automatically close December back to January;
the demo is not evidence of an annual round trip. Interpolation is only a visual effect.

```js
const speciesData = await fetch('/api/data/species').then(r => r.json());
// The backend team must implement this endpoint or serve the files as static assets.
// For a selected GeoJSON feature and an integer month from the slider:
const indices = feature.properties.months
  .map((month, i) => month <= selectedMonth ? i : -1).filter(i => i >= 0);
const trail = indices.map(i => feature.geometry.coordinates[i]);
const position = trail.at(-1);
```

The files are at repository root `data/`; the existing app does not automatically serve
them. Serving endpoints and the website UI are outside this data-only change.

## Obtaining actual observations

The supplied OBIS dataset URL (`https://obis.org/dataset/1cfc4d23-9f`) appears truncated;
it did not resolve during research. Do not cite it as a retrieved dataset.
SWOT confirms that its map contains nesting and telemetry datasets hosted at
OBIS-SEAMAP, with reuse governed by its terms and data request process. No SWOT or
SEAMAP tracks were downloaded or digitised. Access to a map does not itself establish
redistribution permission for every underlying dataset.

A direct OBIS API request failed in the restricted environment and permission for the
network download was declined. Consequently **no actual occurrence or telemetry
records are included** in this handoff. To fetch a small real occurrence sample later:

```powershell
py data/fetch_obis.py --size 100
```

The importer uses standard-library Python and requests up to 100 records per species,
sequentially. It writes the original responses and a separate
`data/obis_sample/occurrences.geojson`. It refuses to overwrite an existing sample.
It has not been verified against a live API response in this environment. A species
may return fewer records or none; the sample is not a representative distribution.
Provider citation, rights, license, dates and uncertainty fields are retained when
available. Missing fields remain null; consult each dataset's metadata for attribution
and licensing before sharing downloaded records.

An OBIS occurrence may represent a sighting, specimen or other record, not necessarily
a live tagged turtle. Never connect independent occurrences into a migration route.
OBIS `bathymetry` means seabed depth, not turtle swimming depth; even reported occurrence
depths require checking the provider's methods. The importer does not infer dive depth.

For real migration trails, obtain permitted individual telemetry datasets with stable
animal/tag IDs, dated coordinates and documented quality flags. Split by individual,
sort timestamps, check gaps and location quality, and retain dataset provenance and
licenses. Only then replace demo features with observed tracks. Coverage of all seven
species is not guaranteed. NOAA's [Kemp's ridley and loggerhead tracking catalog](https://www.fisheries.noaa.gov/inport/item/30696)
is another lead for genuine tracking data; its files have not been downloaded here.

## Validation

```powershell
py data/validate.py
```

Checks cover all seven species, citation references, coordinates, date ordering, month
coverage, array alignment and explicit demo labels. This verifies structural integrity,
not scientific accuracy of synthetic routes. Do not run Python with `-O` for this check.
