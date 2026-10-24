# Sea turtle data handoff

`species.json` contains all seven living species, display colours, geographic summaries,
published depth examples, species facts, regional nesting months and citation IDs.
`sources.json` resolves those IDs to source titles, links and the claims they support.
`animation_sightings.json` supplies a four-year selector, seven species options and
year/month availability metadata. It does **not** contain the four requested annual
migration animations: the supplied OBIS-SEAMAP export contains point occurrences, not
species-identified individual tracks. Only four CC0 July 2006 coordinates are included;
restricted 2010 and 2020 coordinates are deliberately omitted.
`animation_depth_profiles.json` contains depth examples from separate published diving
studies, not from OBIS-SEAMAP. They are study-specific and cannot be joined to the
occurrence locations or used as distance-versus-depth swimming animations.
`animation_species_predictions.json` is a separate, low-confidence regional-prior
guess for those four unidentified sightings. The source observations remain unidentified;
the guess is not a validated classification and does not make a species track. Do not
use speculative assignments in scientific or species-specific animation layers.

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

### Historical tracks

The requested year selector is 2006, 2010, 2015 and 2020. The existing
2025 routes are invented animation fixtures, not historical observations. The
repository does not contain verified individual migration tracks for any of these
years or all seven species. The JSON includes the requested year/species selector
structure, but accurate migration animations cannot be populated from the available
records without inventing tracks.

The [SWOT sea turtle database](https://www.seaturtlestatus.org/online-map-data)
contains contributed telemetry tracks. Its [request form](https://www.seaturtlestatus.org/request-data)
requires an email verification code and acceptance of its data-use terms; the
[Chelonioidea species profile](https://seamap.env.duke.edu/species/948946) likewise
opens a download form rather than exposing track records directly. The files have not
been requested or downloaded here. The NOAA [Kemp's ridley and loggerhead tracking catalog](https://www.fisheries.noaa.gov/inport/item/30696)
describes a 2010 dataset, but its catalog says the data reside on a secure government
network requiring multifactor authentication. These sources do not provide files that
can be used for averages in this repository yet.

### Other repositories checked

- [SEATURTLE.ORG tracking](https://seaturtle.org/tracking/) describes Argos-supported
  tracking tools for researchers. Automated access presents a browser verification
  page; no track export was obtained.
- [IUCN MTSG Regional Management Units](https://www.iucn-mtsg.org/regional-management-units)
  describes population-level boundaries built from multiple evidence types, including
  telemetry. RMUs are population geography, not dated individual trajectories.
- [GBIF](https://www.gbif.org/) exposes occurrence records through its API. A sample
  query for green turtles in 1990 returned preserved specimens, among other record
  types; occurrences do not establish continuous individual movement.
- [OBIS-SEAMAP Chelonioidea](https://seamap.env.duke.edu/species/948946) identifies the
  relevant taxon. Its download flow requires completing the site's form; a user-
  provided export was inspected and only CC0 point coordinates are included here.

OBIS occurrence records can provide dated sightings and coordinates, but separate
sightings are not continuous individual tracks. The user-provided
[OBIS-SEAMAP Chelonioidea export](../references.md#bibliography) contains 1,835
point-observation records dated 2006–2020. Its points CSV has no depth fields, and its
`series_id` field is empty for all records, so it does not link observations into
individual trajectories or provide swimming-depth measurements. The records also
include multiple turtle labels and observation types; do not treat every point as an
identified sea turtle track.

`animation_sightings.json` contains only the four July 2006 records from dataset 1889,
which the supplied archive marks CC0. All four are labelled unidentified turtle
(Chelonioidea), not any of the seven species, and have no depth measurement. Render
them as distinct observation markers in date order if desired; never connect them with a
line or label the animation a migration trajectory.

The separate `animation_species_predictions.json` file assigns a low-confidence
loggerhead regional-prior guess to each of these four points. The points are close in
space and time and contain no species-diagnostic information, so this repeated label
does not mean they were individually identified or are one migrating turtle. Keep
predictions visually distinct from observed species labels and allow them to be hidden.

The archive also contains 114 unidentified-turtle point observations in February and
November 2010, but their datasets are CC-BY and the OBIS-SEAMAP download terms prohibit
redistribution without consent except for CC0 datasets. Its 90 March 2020 points are
nests or poached nests in a CC-BY-NC dataset, not turtles swimming at sea. These
coordinates are not included in the animation JSON. There are no 2015 records in this
export.

OBIS `minimumDepthInMeters`, `maximumDepthInMeters` and `bathymetry` fields are not
automatically measured turtle dive depths. Do not draw lines between independent
sightings, or treat seabed depth as animal depth. Add a historical track only when a
permitted source provides individual IDs, timestamps, coordinates, and documented
depth measurements.

The original user-provided OBIS-SEAMAP archive is not copied into this repository. Its
`datasets_and_citations.csv` contains 57 dataset citation entries and sharing policies.
The archive's terms require individual dataset citations and prohibit redistribution
without consent except for CC0 datasets. Check each contributing dataset's citation and
sharing policy before using its records in a product or publishing derived results.

No SWOT/SEAMAP telemetry tracks are included in this handoff. The separate sample
importer below retrieves OBIS occurrences for exploration, not continuous individual
tracks, and must not be used to create migration trajectories or per-position
turtle-dive-depth charts. To fetch a bounded occurrence sample:

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

For year-by-year monthly averages, first obtain permitted individual tracks with stable
animal/tag IDs, timestamps, coordinates and documented quality flags. Measured dive
depths must be linked to those individuals and times; location-only tracks cannot
produce swimming-depth values. Calculate distance from consecutive valid positions
within each individual track, then calculate monthly metrics per individual before
averaging across individuals. Keep sample sizes and missing months visible, and retain
source provenance, uncertainty and licenses. Do not average independent sightings as
tracks or imply coverage where no usable individuals exist. Coverage of all seven
species and each requested year is not guaranteed.

## Validation

```powershell
py data/validate.py
```

Checks cover all seven species, citation references, coordinates, date ordering, month
coverage, array alignment and explicit demo labels. This verifies structural integrity,
not scientific accuracy of synthetic routes. Do not run Python with `-O` for this check.
