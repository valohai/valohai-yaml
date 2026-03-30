### Changelog

#### [v0.56.0](https://github.com/valohai/valohai-yaml/compare/v0.55.0...v0.56.0)

> 30 March 2026

- Do not serialize empty edge configs or default node error actions [`#207`](https://github.com/valohai/valohai-yaml/pull/207)
- Ensure all Items and Enums are re-exported [`#206`](https://github.com/valohai/valohai-yaml/pull/206)

#### [v0.55.0](https://github.com/valohai/valohai-yaml/compare/v0.54.0...v0.55.0)

> 18 February 2026

- Fix environment-variables sent to API [`#201`](https://github.com/valohai/valohai-yaml/pull/201)

#### [v0.54.0](https://github.com/valohai/valohai-yaml/compare/v0.53.0...v0.54.0)

> 6 February 2026

- Add `deployment` edge type [`#199`](https://github.com/valohai/valohai-yaml/pull/199)
- Add possibility to override runtime_config_preset in pipeline node [`#197`](https://github.com/valohai/valohai-yaml/pull/197)

#### [v0.53.0](https://github.com/valohai/valohai-yaml/compare/v0.52.0...v0.53.0)

> 22 January 2026

- Support task blueprints in pipelines task nodes [`#188`](https://github.com/valohai/valohai-yaml/pull/188)
- Add description to pipeline edges [`#190`](https://github.com/valohai/valohai-yaml/pull/190)
- Inline property title and description [`#191`](https://github.com/valohai/valohai-yaml/pull/191)
- Update linter to require environment with preset in step configuration [`#192`](https://github.com/valohai/valohai-yaml/pull/192)
- Add new edge types [`#187`](https://github.com/valohai/valohai-yaml/pull/187)
- 🔨 Generate Markdown documentation for the JSON schema [`#189`](https://github.com/valohai/valohai-yaml/pull/189)
- 📝 Add slug to runtime config preset property description [`#185`](https://github.com/valohai/valohai-yaml/pull/185)

#### [v0.52.0](https://github.com/valohai/valohai-yaml/compare/v0.51.0...v0.52.0)

> 12 December 2025

- Parse runtime config preset ID from YAML config [`#183`](https://github.com/valohai/valohai-yaml/pull/183)

#### [v0.51.0](https://github.com/valohai/valohai-yaml/compare/v0.50.1...v0.51.0)

> 26 November 2025

- Add `cache-volumes` to step definition [`#178`](https://github.com/valohai/valohai-yaml/pull/178)

#### [v0.50.1](https://github.com/valohai/valohai-yaml/compare/v0.50.0...v0.50.1)

> 30 October 2025

- Add support for non-local steps in PipelineConverter too [`#177`](https://github.com/valohai/valohai-yaml/pull/177)

#### [v0.50.0](https://github.com/valohai/valohai-yaml/compare/v0.49.0...v0.50.0)

> 14 October 2025

- Support specifying commit in execution/task node definition [`#175`](https://github.com/valohai/valohai-yaml/pull/175)

#### [v0.49.0](https://github.com/valohai/valohai-yaml/compare/v0.48.0...v0.49.0)

> 4 September 2025

- Add `reuse-children` to Tasks [`#174`](https://github.com/valohai/valohai-yaml/pull/174)
- Allow configuring deployments for auto-create [`#173`](https://github.com/valohai/valohai-yaml/pull/173)

#### [v0.48.0](https://github.com/valohai/valohai-yaml/compare/v0.47.1...v0.48.0)

> 23 June 2025

- Demote duplicate name error to warning [`#171`](https://github.com/valohai/valohai-yaml/pull/171)
- Inline JSON Schema in code [`#170`](https://github.com/valohai/valohai-yaml/pull/170)

#### [v0.47.1](https://github.com/valohai/valohai-yaml/compare/v0.47.0...v0.47.1)

> 27 May 2025

- Really become 0.47.1 [`#169`](https://github.com/valohai/valohai-yaml/pull/169)

#### [v0.47.0](https://github.com/valohai/valohai-yaml/compare/v0.46.0...v0.47.0)

> 23 May 2025

- Add linter error for duplicate names [`#164`](https://github.com/valohai/valohai-yaml/pull/164)
- Add `tolerations` to endpoint definition [`#167`](https://github.com/valohai/valohai-yaml/pull/167)
- Introduce environment_variable_groups to Step class [`#160`](https://github.com/valohai/valohai-yaml/pull/160)

#### [v0.46.0](https://github.com/valohai/valohai-yaml/compare/v0.45.0...v0.46.0)

> 15 January 2025

- Elide default reuse-executions and edge-merge-mode values from serialization result [`#159`](https://github.com/valohai/valohai-yaml/pull/159)

#### [v0.45.0](https://github.com/valohai/valohai-yaml/compare/v0.44.0...v0.45.0)

> 3 January 2025

- Ensure shebang lines are passed through as expected; add `join_command` helper [`#158`](https://github.com/valohai/valohai-yaml/pull/158)

#### [v0.44.0](https://github.com/valohai/valohai-yaml/compare/v0.43.0...v0.44.0)

> 29 November 2024

- Implement new step.inputs[].download configuration [`#157`](https://github.com/valohai/valohai-yaml/pull/157)

#### [v0.43.0](https://github.com/valohai/valohai-yaml/compare/v0.42.0...v0.43.0)

> 4 November 2024

- Add some regression tests

#### [v0.42.0](https://github.com/valohai/valohai-yaml/compare/v0.41.0...v0.42.0)

> 20 September 2024

- Add Retry node error action [`4b6c733`](https://github.com/valohai/valohai-yaml/commit/4b6c733a851172a5466048b2b44be43de574a5c4)

#### [v0.41.0](https://github.com/valohai/valohai-yaml/compare/v0.40.0...v0.41.0)

> 30 August 2024

- Add edge-merge-mode property in node [`#153`](https://github.com/valohai/valohai-yaml/pull/153)

#### [v0.40.0](https://github.com/valohai/valohai-yaml/compare/v0.39.0...v0.40.0)

> 3 June 2024

- Added `reuse-executions` property to pipeline schema [`#152`](https://github.com/valohai/valohai-yaml/pull/152)
- Support list as pipeline parameter expression [`#147`](https://github.com/valohai/valohai-yaml/pull/147)

#### [v0.39.0](https://github.com/valohai/valohai-yaml/compare/v0.38.0...v0.39.0)

> 13 March 2024

- Parameter categories [`#149`](https://github.com/valohai/valohai-yaml/pull/149)
- Warn but don't die if a pipeline parameter is missing targets [`#144`](https://github.com/valohai/valohai-yaml/pull/144)

#### [v0.38.0](https://github.com/valohai/valohai-yaml/compare/v0.37.0...v0.38.0)

> 19 December 2023

- Parse and serialize Step resources as WorkloadResources [`#140`](https://github.com/valohai/valohai-yaml/pull/140)

#### [v0.37.0](https://github.com/valohai/valohai-yaml/compare/v0.36.0...v0.37.0)

> 23 November 2023

- Add error-pipeline as then-action for node actions [`#139`](https://github.com/valohai/valohai-yaml/pull/139)
- Order bayesian-only props for stable error snapshot [`#138`](https://github.com/valohai/valohai-yaml/pull/138)
- Add lint warnings for nonsensical Task configurations [`#136`](https://github.com/valohai/valohai-yaml/pull/136)
- Add Task.parameter-sets [`#135`](https://github.com/valohai/valohai-yaml/pull/135)
- Preserve workload resources structure on serialization [`#133`](https://github.com/valohai/valohai-yaml/pull/133)
- Add Task.parameter-sets (#135) [`#134`](https://github.com/valohai/valohai-yaml/issues/134)

#### [v0.36.0](https://github.com/valohai/valohai-yaml/compare/v0.35.0...v0.36.0)

> 30 October 2023

- Task: add remaining fields (maximum queued executions, on child error) [`#132`](https://github.com/valohai/valohai-yaml/pull/132)
- Kebab-case task properties and make task type validation more lenient [`#131`](https://github.com/valohai/valohai-yaml/pull/131)
- Add task-presets to serializer to expose via commit with config [`#128`](https://github.com/valohai/valohai-yaml/pull/128)
- Task: add remaining fields (maximum queued executions, on child error) (#132) [`#90`](https://github.com/valohai/valohai-yaml/issues/90)

#### [v0.35.0](https://github.com/valohai/valohai-yaml/compare/v0.34.0...v0.35.0)

> 19 October 2023

- Add upload-store to step [`#124`](https://github.com/valohai/valohai-yaml/pull/124)
- Add stop-condition field to Step and Task objects [`#127`](https://github.com/valohai/valohai-yaml/pull/127)

#### [v0.34.0](https://github.com/valohai/valohai-yaml/compare/v0.33.0...v0.34.0)

> 16 October 2023

- Omit None parameters [`#126`](https://github.com/valohai/valohai-yaml/pull/126)
- Validating empty values as int/float gives more specific error [`#112`](https://github.com/valohai/valohai-yaml/pull/112)

#### [v0.33.0](https://github.com/valohai/valohai-yaml/compare/v0.32.0...v0.33.0)

> 22 September 2023

- More lenient Override parsing [`#118`](https://github.com/valohai/valohai-yaml/pull/118)
- Be a little more lenient when parsing legacy overrides [`5b03c6e`](https://github.com/valohai/valohai-yaml/commit/5b03c6e7e1975c455989ba84498009c3b08ea682)
- Add lint(..., validate_schema=False) [`8b42700`](https://github.com/valohai/valohai-yaml/commit/8b42700dedf27a909754799ce106c24f75d10e5f)

#### [v0.32.0](https://github.com/valohai/valohai-yaml/compare/v0.31.0...v0.32.0)

> 4 September 2023

- Do not keep empty Node `override` in serialized output [`#113`](https://github.com/valohai/valohai-yaml/pull/113)

#### [v0.31.0](https://github.com/valohai/valohai-yaml/compare/v0.30.0...v0.31.0)

> 21 August 2023

- Pipeline Parameters: use non-None falsy defaults as is in conversion [`#111`](https://github.com/valohai/valohai-yaml/pull/111)
- Pipeline Parameter Conversion [`#107`](https://github.com/valohai/valohai-yaml/pull/107)
- Add Makefile for development shortcuts [`#109`](https://github.com/valohai/valohai-yaml/pull/109)

#### [v0.30.0](https://github.com/valohai/valohai-yaml/compare/v0.29.1...v0.30.0)

> 11 August 2023

- Merge inputs and parameters in Override class [`#105`](https://github.com/valohai/valohai-yaml/pull/105)
- Do not serialize multiple-separator for parameters that do not support it [`#106`](https://github.com/valohai/valohai-yaml/pull/106)
- Do not serialize multiple-separator for parameters that do not support it [`#92`](https://github.com/valohai/valohai-yaml/issues/92)

#### [v0.29.1](https://github.com/valohai/valohai-yaml/compare/v0.29.0...v0.29.1)

> 3 August 2023

- Execution Node: move runtime configs in runtime_config [`#104`](https://github.com/valohai/valohai-yaml/pull/104)
- Update JSON Schema to Draft 2020-12 [`#102`](https://github.com/valohai/valohai-yaml/pull/102)

#### [v0.29.0](https://github.com/valohai/valohai-yaml/compare/v0.28.0...v0.29.0)

> 7 July 2023

- Add a custom id_of to make things work with JSONSchema 4.18 too [`#101`](https://github.com/valohai/valohai-yaml/pull/101)
- Add task template [`#98`](https://github.com/valohai/valohai-yaml/pull/98)
- Improve error messages for indentation errors [`#94`](https://github.com/valohai/valohai-yaml/pull/94)
- Fix alphabetically sorted steps [`#93`](https://github.com/valohai/valohai-yaml/pull/93)

#### [v0.28.0](https://github.com/valohai/valohai-yaml/compare/v0.27.0...v0.28.0)

> 3 February 2023

- Add support for parameter UI widgets [`#89`](https://github.com/valohai/valohai-yaml/pull/89)

#### [v0.27.0](https://github.com/valohai/valohai-yaml/compare/v0.26.0...v0.27.0)

> 24 January 2023

- Add step icon + category [`#87`](https://github.com/valohai/valohai-yaml/pull/87)
- Node selector and required devices to endpoints [`#85`](https://github.com/valohai/valohai-yaml/pull/85)

#### [v0.26.0](https://github.com/valohai/valohai-yaml/compare/v0.25.2...v0.26.0)

> 3 January 2023

- Add time-limit and no-output-timeout to step parsing [`#83`](https://github.com/valohai/valohai-yaml/pull/83)
- Allow using `parameter-value` with falsy but extant values [`#79`](https://github.com/valohai/valohai-yaml/pull/79)

#### [v0.25.2](https://github.com/valohai/valohai-yaml/compare/v0.25.1...v0.25.2)

> 8 September 2022

- Similarly to node actions, don't serialize empty pipeline parameters [`b5b4da7`](https://github.com/valohai/valohai-yaml/commit/b5b4da7e48023884e35f3c133ade8791d8cb1b4b)

#### [v0.25.1](https://github.com/valohai/valohai-yaml/compare/v0.25.0...v0.25.1)

> 8 September 2022

- Don't require parameters when programmatically constructing pipelines [`4af83a2`](https://github.com/valohai/valohai-yaml/commit/4af83a2c0a0cd6efcbefdf98c0e36690bc57aa02)

#### [v0.25.0](https://github.com/valohai/valohai-yaml/compare/v0.24.0...v0.25.0)

> 7 September 2022

- Pipeline: add pipeline level parameters [`cedd4e5`](https://github.com/valohai/valohai-yaml/commit/cedd4e53ffd80eebd6a68096292a82670052bc5b)

#### [v0.24.0](https://github.com/valohai/valohai-yaml/compare/v0.23.0...v0.24.0)

> 15 August 2022

- Pipeline: fix parameter override by step and node [`#72`](https://github.com/valohai/valohai-yaml/pull/72)

#### [v0.23.0](https://github.com/valohai/valohai-yaml/compare/v0.22.0...v0.23.0)

> 23 February 2022

- Use real exceptions instead of assertions for certain type checks [`#70`](https://github.com/valohai/valohai-yaml/pull/70)

#### [v0.22.0](https://github.com/valohai/valohai-yaml/compare/v0.21.1...v0.22.0)

> 14 February 2022

- Add on-error enum string to Pipeline Nodes [`#66`](https://github.com/valohai/valohai-yaml/pull/66)

#### [v0.21.1](https://github.com/valohai/valohai-yaml/compare/v0.21.0...v0.21.1)

> 22 December 2021

- Correct order of applying overrides to step data when converting nodes [`265927a`](https://github.com/valohai/valohai-yaml/commit/265927a825d5bda319704d2a5209e4d1765e76d8)

#### [v0.21.0](https://github.com/valohai/valohai-yaml/compare/v0.20.1...v0.21.0)

> 15 December 2021

- Pipeline conversion API [`#61`](https://github.com/valohai/valohai-yaml/pull/61)

#### [v0.20.1](https://github.com/valohai/valohai-yaml/compare/v0.20.0...v0.20.1)

> 4 November 2021

- Correct return type for merge_with [`#58`](https://github.com/valohai/valohai-yaml/pull/58)
- Do not keep empty Node `actions` in serialized output [`#59`](https://github.com/valohai/valohai-yaml/pull/59)

#### [v0.20.0](https://github.com/valohai/valohai-yaml/compare/v0.16.0...v0.20.0)

> 22 October 2021

- Handle empty YAML files in parse() [`#56`](https://github.com/valohai/valohai-yaml/pull/56)
- Add optional `resources` to endpoint definition [`b6dbcf3`](https://github.com/valohai/valohai-yaml/commit/b6dbcf3d8caf33499a9152a121f4eddedd241829)

#### [v0.16.0](https://github.com/valohai/valohai-yaml/compare/v0.15.0...v0.16.0)

> 30 September 2021

- Do re-exports in init modules [`#52`](https://github.com/valohai/valohai-yaml/pull/52)
- Increase endpoint name validation [`2df0825`](https://github.com/valohai/valohai-yaml/commit/2df0825191055f54ecc7c3d7af8710a0491183f8)
- Raise a ValidationError when an edge specifier (a.b.c) has the wrong number of items [`29221bc`](https://github.com/valohai/valohai-yaml/commit/29221bc6a58f16bfafc7a147c64f9d81a12f9bd0)

#### [v0.15.0](https://github.com/valohai/valohai-yaml/compare/v0.14.1...v0.15.0)

> 8 July 2021

- Pipeline node actions [`#48`](https://github.com/valohai/valohai-yaml/pull/48)
- Drop LegacyParameterMap (a relic from 2018) [`#44`](https://github.com/valohai/valohai-yaml/pull/44)
- Bad shorthand edge validation [`#43`](https://github.com/valohai/valohai-yaml/pull/43)
- Add task-node.yaml schema [`#42`](https://github.com/valohai/valohai-yaml/pull/42)

#### [v0.14.1](https://github.com/valohai/valohai-yaml/compare/v0.14.0...v0.14.1)

> 17 March 2021

- Add initial pipeline task node model (exactly like execution at this point) [`ddc1ed3`](https://github.com/valohai/valohai-yaml/commit/ddc1ed38e30a6da69b3866b1144f083f020a5e27)

#### [v0.14.0](https://github.com/valohai/valohai-yaml/compare/v0.13.0...v0.14.0)

> 15 March 2021

- Extend mount objects with `type` and `options` [`#37`](https://github.com/valohai/valohai-yaml/pull/37)

#### [v0.13.0](https://github.com/valohai/valohai-yaml/compare/v0.12.0...v0.13.0)

> 30 October 2020

- Simple default config merging + ability to provide custom merging strategy [`#35`](https://github.com/valohai/valohai-yaml/pull/35)

#### [v0.12.0](https://github.com/valohai/valohai-yaml/compare/v0.11.1...v0.12.0)

> 19 October 2020

- Allow deployments as pipeline nodes [`ca682f4`](https://github.com/valohai/valohai-yaml/commit/ca682f4dcdd853f2050ccc1ba20ea8ffdc8f5f69)
- Add warning-level linting for invalid parameter defaults [`3a10188`](https://github.com/valohai/valohai-yaml/commit/3a1018899b1489b54906dc764cd6373711446fe3)
- Add --strict-warnings mode to CLI [`fab78cc`](https://github.com/valohai/valohai-yaml/commit/fab78cc46c862108d3595e3ac2f8a3a315ffbf5d)

#### [v0.11.1](https://github.com/valohai/valohai-yaml/compare/v0.11.0...v0.11.1)

> 24 June 2020

- Remove trailing comma not compatible with Python 3.5 [`9bb48f4`](https://github.com/valohai/valohai-yaml/commit/9bb48f43c5b7b026d74710860e5427c4e0ec71dd)

#### [v0.11.0](https://github.com/valohai/valohai-yaml/compare/v0.10.0...v0.11.0)

> 16 June 2020

- New Input features: Keep directories & forced filename [`#29`](https://github.com/valohai/valohai-yaml/pull/29)
- Add Input.keep-directories [`a61ea21`](https://github.com/valohai/valohai-yaml/commit/a61ea216b4342bbd5474645cc96ccc5abc498fb5)
- Add Input.filename [`36c3cb2`](https://github.com/valohai/valohai-yaml/commit/36c3cb2d2c87a60bc6f591db69c89b7286a90a99)

#### [v0.10.0](https://github.com/valohai/valohai-yaml/compare/v0.9.1...v0.10.0)

> 2 January 2020

- Parameter additions [`#26`](https://github.com/valohai/valohai-yaml/pull/26)
- Drop Python 2 support for good [`#25`](https://github.com/valohai/valohai-yaml/pull/25)
- Add list parameters [`c2c1f2a`](https://github.com/valohai/valohai-yaml/commit/c2c1f2a3afc91c98037a5c9b8a576c03d8e3c25c)
- Add pass-true-as/pass-false-as for flag (boolean) parameters [`1c891db`](https://github.com/valohai/valohai-yaml/commit/1c891db1278b30df4bd75bae0224575753ea8e47)

#### [v0.9.1](https://github.com/valohai/valohai-yaml/compare/v0.9...v0.9.1)

> 22 August 2019

- Stringify values before quoting for `parameter-value` [`#23`](https://github.com/valohai/valohai-yaml/pull/23)
- Allow unknown elements on the top level of the configuration [`#22`](https://github.com/valohai/valohai-yaml/pull/22)
- Pipeline improvements [`#20`](https://github.com/valohai/valohai-yaml/pull/20)
- Modernize the pipeline example slightly [`26bfaa3`](https://github.com/valohai/valohai-yaml/commit/26bfaa36c50575c9ab42021aca58a1d48cd89b76)
- Improve Config.lint() API [`cd0504c`](https://github.com/valohai/valohai-yaml/commit/cd0504cafd3f0cfa46316a4a8c30dec521be1bdf)
- Add linting for pipeline step existence [`9c05830`](https://github.com/valohai/valohai-yaml/commit/9c058304c9ad1ad8c9220bc9f098a9dcf80700b9)

#### [v0.9](https://github.com/valohai/valohai-yaml/compare/v0.8.1...v0.9)

> 31 July 2019

- Add initial objects for pipelines [`#19`](https://github.com/valohai/valohai-yaml/pull/19)

#### [v0.8.1](https://github.com/valohai/valohai-yaml/compare/v0.8.0...v0.8.1)

> 4 June 2019

- Add descriptions to steps [`#18`](https://github.com/valohai/valohai-yaml/pull/18)
- Fix Step.serialize() regression [`#17`](https://github.com/valohai/valohai-yaml/pull/17)
- Miscellaneous little improvements [`#16`](https://github.com/valohai/valohai-yaml/pull/16)
- Deprecate Python 2 [`#15`](https://github.com/valohai/valohai-yaml/pull/15)
- Reformat syntax on all YAML files so they are uniform [`2640336`](https://github.com/valohai/valohai-yaml/commit/264033654defbaeb74847ed7d2fc6d8cbb4b985d)
- Teach objects how to lint themselves [`2254412`](https://github.com/valohai/valohai-yaml/commit/2254412265668709f0f185e5838bb22e16435aed)

#### [v0.8.0](https://github.com/valohai/valohai-yaml/compare/v0.7.1...v0.8.0)

> 14 February 2019

- Schema additions [`#12`](https://github.com/valohai/valohai-yaml/pull/12)
- Fix optional flag parsing (fixes #935) [`#935`](https://github.com/valohai/valohai-yaml/issues/935)
- Schema: add environment variables to steps [`b2b7b45`](https://github.com/valohai/valohai-yaml/commit/b2b7b45bf4533551d14240961c6b3fc2e0aec38f)
- Move linting logic from valohai-cli to valohai-yaml for reusability [`e250820`](https://github.com/valohai/valohai-yaml/commit/e250820e4b087652ec2316994918529bc805074d)

#### [v0.7.1](https://github.com/valohai/valohai-yaml/compare/v0.7...v0.7.1)

> 29 August 2018

- Add descriptions to inputs [`#11`](https://github.com/valohai/valohai-yaml/pull/11)
- Add description property to inputs [`fa2b704`](https://github.com/valohai/valohai-yaml/commit/fa2b704791b1a9d33aadebb7ede5d8b8390f32df)
- Explicitly note that optional is false by default (i.e. all parameters or inputs are required by default) [`780d68f`](https://github.com/valohai/valohai-yaml/commit/780d68f37e072022481ce9733552a739d393dae8)

#### [v0.7](https://github.com/valohai/valohai-yaml/compare/v0.6.1...v0.7)

> 16 July 2018

- Add support for {parameter:...} and {parameter-value:...} interpolations [`#9`](https://github.com/valohai/valohai-yaml/pull/9)
- Don't use gcr.io/ image urls in examples [`a5d4bde`](https://github.com/valohai/valohai-yaml/commit/a5d4bde17dfdc83ee996fb8a8225fb2b0fb4e865)

#### [v0.6.1](https://github.com/valohai/valohai-yaml/compare/v0.6...v0.6.1)

> 25 April 2018

- Embetter support for shell variable interpolation [`#8`](https://github.com/valohai/valohai-yaml/pull/8)
- Ensure non-existent curly segments are passed through as is by build_command [`d82d477`](https://github.com/valohai/valohai-yaml/commit/d82d477faa58a31e7bb04faffed96e08a10c7f12)

#### [v0.6](https://github.com/valohai/valohai-yaml/compare/v0.5...v0.6)

> 4 April 2018

- Add deployment endpoints [`#7`](https://github.com/valohai/valohai-yaml/pull/7)
- Become 0.6 and add version to **init**.py according to PEP 396 [`eb3ece4`](https://github.com/valohai/valohai-yaml/commit/eb3ece4849d3de088f7699ab7a0a6242d74e4457)
- Add author_email [`ca7f678`](https://github.com/valohai/valohai-yaml/commit/ca7f678e12dc1654c54dfb5c76506551b37c810c)

#### [v0.5](https://github.com/valohai/valohai-yaml/compare/v0.4...v0.5)

> 1 March 2017

- Add support for `mounts` stanzas [`#6`](https://github.com/valohai/valohai-yaml/pull/6)

#### [v0.4](https://github.com/valohai/valohai-yaml/compare/v0.3.1...v0.4)

> 3 February 2017

- Convert schemata to YAML for easier writing [`68bfa49`](https://github.com/valohai/valohai-yaml/commit/68bfa496f0f75a9e6b77cf377ffb80472aa72fdd)
- Add support for boolean-type flag parameters [`72d2d66`](https://github.com/valohai/valohai-yaml/commit/72d2d66ffaf5d89873e96936053a7b5063ccdfa4)
- DRY out roundtrip config fixtures into `config_fixture` factory [`67fc615`](https://github.com/valohai/valohai-yaml/commit/67fc6156de522e83af7c2f9ac1eb22f611da0fca)

#### [v0.3.1](https://github.com/valohai/valohai-yaml/compare/v0.3...v0.3.1)

> 25 January 2017

- Add optional property to inputs [`#4`](https://github.com/valohai/valohai-yaml/pull/4)

#### [v0.3](https://github.com/valohai/valohai-yaml/compare/v0.2...v0.3)

> 19 January 2017

- Improved validation and parsing [`#3`](https://github.com/valohai/valohai-yaml/pull/3)
- Graduate `Parameter` and `Input` into realer objects [`0ef4af8`](https://github.com/valohai/valohai-yaml/commit/0ef4af80ea9ddbbd93be0bb801ac0181ebb40286)
- Add .validate api to parameters [`f407a3a`](https://github.com/valohai/valohai-yaml/commit/f407a3a339a1bf3e3935b70237998399ea988f13)
- Improve schema and be stricter about it [`6320743`](https://github.com/valohai/valohai-yaml/commit/63207437ed3024a98e270cb78fd6efbb428ccb86)

#### v0.2

> 17 January 2017

- Add parsing! [`#2`](https://github.com/valohai/valohai-yaml/pull/2)
- Initial code [`#1`](https://github.com/valohai/valohai-yaml/pull/1)
