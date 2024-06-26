# Academic Award Datasets

[![license](https://img.shields.io/badge/License-MIT-brightscreen)](https://github.com/xiaohk/academic-award/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11732208.svg)](https://doi.org/10.5281/zenodo.11732208)

Recipient datasets of academic awards, including ACM Fellow, IEEE Fellow, NAS
Members, AAAI Fellow, and AAAS Fellow.

| Award                                                                      | Description                                                                                                                             | Fields                                                       |     Years | Number |
| :------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------- | --------: | -----: |
| [AAA&S Members](./data/amacad-members.json)                                | [Members of American Academy of Arts and Sciences](https://www.amacad.org/members)                                                      | `name`, `affiliation`, `area`, `specialty`,`year`            | 1780–2023 | 14,876 |
| [AAAI Fellows](./data/aaai-fellows.json)                                   | [Association for the Advancement of Artificial Intelligence Fellows](https://aaai.org/about-aaai/aaai-awards/the-aaai-fellows-program/) | `name`, `affiliation`, `contribution`, `year`                | 1990–2024 |    350 |
| [AAAS Fellows](./data/aaas-fellows.json)                                   | [American Association for the Advancement of Science Honorary Fellows](https://www.aaas.org/fellows)                                    | `name`, `year`, `state`, `country`, `affiliation`, `primary` | 1955–2023 |  9,027 |
| [ACM Dissertation Award](./data/acm-dissertation-award.json)               | [Association for Computing Doctoral Dissertation Award](https://awards.acm.org/doctoral-dissertation/nominations)                       | `name`, `year`                                               | 1978–2022 |    121 |
| [ACM Distinguished Members](./data/acm-distinguished-member.json)          | [Association for Computing Distinguished Members](https://awards.acm.org/distinguished-members)                                         | `name`, `year`                                               | 2006–2023 |    914 |
| [ACM Fellows](./data/acm-fellow.json)                                      | [Association for Computing Machinery Fellows](https://awards.acm.org/fellows)                                                           | `name`, `year`                                               | 1994–2023 |  1,512 |
| [ACM Gordon Bell Prize](./data/acm-gordon-bell-prize.json)                 | [Association for Computing Gordon Bell Prize](https://awards.acm.org/bell)                                                              | `name`, `year`                                               | 2006–2023 |    365 |
| [ACM Grace Murray Hopper Award](./data/acm-grace-murray-hopper-award.json) | [Association for Computing Grace Murray Hopper Award](https://awards.acm.org/hopper)                                                    | `name`, `year`                                               | 1971–2022 |     51 |
| [ACM Senior Members](./data/acm-senior-member.json)                        | [Association for Computing Senior Members](https://awards.acm.org/senior-members)                                                       | `name`, `year`                                               | 2006–2024 |  3,348 |
| [ACM Turing Award](./data/acm-turing-award.json)                           | [Association for Computing A.M. Turing Award](https://amturing.acm.org/)                                                                | `name`, `year`                                               | 1966–2023 |     77 |
| [IEEE Fellows](./data/ieee-fellows.json)                                   | [Institute of Electrical and Electronics Engineers Fellow Program](https://www.ieee.org/membership/fellows/index.html)                  | `name`, `year`, `region`, `category`, `citation`             | 1964–2024 |  7,523 |
| [NAS Member](./data/nas-members.json)                                      | [National Academy of Sciences Member](https://www.nasonline.org/membership/)                                                            | `name`, `year`, `affiliation`, `primary`, `secondary`        | 1962–2023 |  3,108 |

## Contribution

Your contribution is appreciated! Please submit a PR to update existing award
recipient lists or add new ones. The scraping scripts can be found in the root
folder.

## Citation

If you find these datasets useful, please consider citing them.

```bibtex
@misc{wangAcademicAwardRecipient2024,
  title = {Academic {{Award Recipient Datasets}}},
  author = {Wang, Zijie J.},
  year = {2024},
  doi = {10.5281/ZENODO.11732208},
  url = {https://zenodo.org/doi/10.5281/zenodo.11732208},
  urldate = {2024-06-16},
  copyright = {Creative Commons Attribution 4.0 International},
  howpublished = {Zenodo}
}
```

## License

The software and datasets are available under the [MIT License](./LICENSE).

## Contact

If you have any questions, feel free to
[open an issue](https://github.com/xiaohk/academic-award/issues/new) or contact
[Jay Wang](https://zijie.wang).
