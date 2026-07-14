# IEEE Reference Style Guide for Authors — rules digest

Repo-side documentation; not installed with the skill. This digest records the reference-style
rules from the *IEEE Reference Style Guide for Authors* (IEEE Publication Operations,
V 3.28.2025) that inform the skill, so their provenance survives independently of the source
document.

- Source: IEEE Publication Operations, *IEEE Reference Style Guide for Authors*, V 3.28.2025
  (https://journals.ieeeauthorcenter.ieee.org/). Accessed 14 July 2026 via a published copy
  supplied by the maintainer.
- Encoded in the skill: "IEEE reference style essentials" in
  [`venue-guidance.md`](../../skills/ieee-acm-paper-writing/references/venue-guidance.md).
- Precedence: the current edition of the guide and venue-specific author instructions override
  everything below.
- Not reproduced here: the guide's List of Publishers and the abbreviations of periodicals with
  non-English titles. Consult the source document for those lists.

## Citing references in text

- References need not be cited in text; when they are, they appear on the line, in square
  brackets, inside the punctuation, and may be treated grammatically as nouns: "according to
  [1]"; "as shown by Brown [4], [5]"; "Smith [4] and Brown and Jones [5]"; "Wood et al. [7]."
- Reference ranges are written out with no en dash: "[1], [2], [3], [4]," never "[1]–[4]."
- Use "et al." in text when three or more names are given for a cited reference.
- Eliminate "ibid." and "op. cit."; cite the earlier reference number instead and renumber the
  reference section accordingly.
- Citing parts of a reference: [3, Thm. 1]; [3, Lemma 2]; [3, pp. 5–10]; [3, eq. (2)];
  [3, Fig. 1]; [3, Appendix I]; [3, Sect. 4.5]; [3, Ch. 2, pp. 5–10]; [3, Algorithm 5].

## Reference-list mechanics

- Reference numbers are set flush left, on the line, enclosed in square brackets, forming a
  hanging column of their own beyond the body of the reference.
- Given names of authors and editors are abbreviated to initials preceding the last name. No
  commas around Jr., Sr., and III (Michael Smith Jr.).
- IEEE publications list all authors up to six names; with more than six, use the primary
  author's name followed by "et al." For non-IEEE publications, "et al." may be used when
  additional names are not provided.
- All references end with a period except those ending with a URL. When a reference contains
  both a DOI or accessed date and a URL, the DOI or accessed date is placed first, followed by a
  period, then the URL without a final period.
- All references must include at least the year of publication (or of access). With no date,
  use "(n.d.)" in the date position, preceded and followed by periods.
- Two months for the same issue are separated by a slash (Jul./Aug.), followed by the year.
- Do not combine references; there must be only one reference with each number.
- When citing IEEE Transactions, verify the issue number and month on IEEE Xplore; not all IEEE
  publications include them. Early access articles use the date of publication; articles
  published within a volume use the volume and issue publication date.
- Prior to 1988, IEEE Transactions/Journals volume numbers carried the journal acronym
  (vol. AC-26); the only exception is *Proceedings of the IEEE*, which never carried one.
  *Proc. Inst. Elect. Eng.* (U.K.) must not be confused with *Proc. IEEE*.

## Basic formats by source type

Skeletons as given by the guide; italicized titles follow the venue template.

### Periodicals

- `J. K. Author, "Name of paper," Abbrev. Title of Periodical, vol. x, no. x, pp. xxx–xxx,
  Abbrev. Month, year, doi: xxx.`
- Article ID instead of page range: `..., Abbrev. Month, year, Art. no. xxx.` A page number that
  looks "wrong" (one long number, non-sequential range, or a 1–XX range with a volume number)
  may be an article ID; query the author.
- Early access: `J. K. Author, "Name of paper," Abbrev. Title of Periodical, early access,
  Month day, year, doi: xxx.` Once an article is in advance online access at the publisher, cite
  that version — the version of record — not the arXiv version. The DOI is essential as it will
  not change.
- Accepted or scheduled but not yet published (and not early access): end with
  `..., to be published.` Do not use "to appear in."
- Not yet accepted: end with `..., submitted for publication.`
- Other language: insert `(in Language)` after the paper title; a translation source may follow
  in parentheses at the end.
- Online: append `Accessed: Month Day, Year, doi: xxx. [Online]. Available: site/path/file`.
- Virtual journal: `Name(s) of Ed(s)., "Title of Issue," in Title of Journal, Abbrev. month
  year. [Online]. Available: URL`.
- Periodical titles of only one word (Science, Nature) are spelled out, never abbreviated.

### Conferences and conference proceedings

- Paper presented at a conference: `J. K. Author, "Title of paper," presented at the Abbrev.
  Name of Conf., City of Conf., Abbrev. State, Country, Month and day(s), year, Paper number.`
- Proceedings in print: `J. K. Author, "Title of paper," in Abbrev. Name of Conf., (location
  optional), (Month and day(s) if provided) year, pp. xxx–xxx.` If the year is in the conference
  title, it may be omitted from the end. All published conference or proceedings papers have
  page numbers.
- With DOI: `..., year, pp. xxx–xxx, doi: xxx.`
- With editors: insert `X. Editor, Ed.` after the conference name.
- Online: end with `[Online]. Available: http://www.url.com`; presented-paper online form is
  `J. K. Author. (Date). Title. Presented at Abbreviated Conf. title. [Type of Medium].
  Available: site/path/file`.
- Conference-name words are abbreviated (see table below); write out remaining words but omit
  most articles and prepositions ("of the," "on"): *Proceedings of the 1996 Robotics and
  Automation Conference* becomes *Proc. 1996 Robot. Automat. Conf.* Ordinals in conference names
  use the numerical form ("1st," not "First"). Include the location if given; U.S. locations
  carry "USA" after city and state.

| Word | Abbreviation | Word | Abbreviation |
| --- | --- | --- | --- |
| Annals | Ann. | Proceedings | Proc. |
| Annual | Annu. | Record | Rec. |
| Colloquium | Colloq. | Symposium | Symp. |
| Conference | Conf. | Technical Digest | Tech. Dig. |
| Congress | Congr. | Technical Paper | Tech. Paper |
| Convention | Conv. | Workshop | Workshop |
| Digest | Dig. | First | 1st |
| Exposition | Expo. | Second | 2nd |
| International | Int. | Third | 3rd |
| Meeting | Meeting | Fourth/nth… | 4th/nth… |
| National | Nat. | | |

### Books

- Book: `J. K. Author, "Title of chapter in the book," in Title of Published Book, xth ed. City
  of Publisher, (only U.S. State), Country: Abbrev. of Publisher, year, ch. x, sect. x,
  pp. xxx–xxx.`
- Online: append `[Online]. Available: http://www.web.com` (with `Accessed:` date when used).
- Foreign publication, not translated: add `(in Language)` after the publisher.
- Translated: credit as `trans. J. K. Translator` after the book title.
- With editors: `X. Editor, Ed.,` (or `Eds.`) after the book title; an edited volume cited as a
  whole is `X. Editor, Ed. Title of Published Book. City, State, Country: Publisher, year.`
- With series title: series in parentheses after the book title —
  `Title of Published Book (Title of the Series), X. Editor, Ed., xth ed. ...`

### Courses and lectures

- Course: `Name of University. (Year). Title of course. [Online]. Available: URL`
- Coursepack: `J. K. Instructor. Title of coursepack. (Semester). Title of course.
  University/Publisher location: University/Publisher name.`
- Lecture notes: `J. K. Author. (Year). Title of lecture [Type of Medium]. Available: URL`
- Lecture online: `University name. (year). Title of lecture. [Type of Medium]. Available: URL`

### Datasets

- Essential components: author names of each individual or organizational entity responsible for
  the dataset; date published or disseminated; complete title including edition or version;
  publisher and/or distributor; electronic location or identifier (URL or DOI). Append the date
  retrieved if the title and locator are not specific to the exact instance used.
- With DOI: `Author, Date, "Title of Dataset," Source, doi: xxx.`
- With DOI resolver: `Author, Date, "Title of Dataset," Source, doi: URL.`
- With website address: `Author, Date, "Title of Dataset," Source. [Online]. Available: URL`
- IEEE follows the FORCE11 Data Citation Principles: importance (data are citable products of
  research), credit and attribution, evidence (cite data wherever a claim relies on it), unique
  identification (persistent, machine-actionable, globally unique identifier), access,
  persistence (identifiers and metadata outlive the data), specificity and verifiability (the
  exact timeslice/version retrieved must be verifiable), and interoperability and flexibility.

### Handbooks and manuals

- Handbook/manual in print: `Name of Manual/Handbook, x ed., Abbrev. Name of Co., City of Co.,
  Abbrev. State, Country, year, pp. xxx–xxx.`
- Manual online: `J. K. Author (or Abbrev. Name of Co., City, State, Country). Name of
  Manual/Handbook, x ed. (year). Accessed: Date. [Online]. Available: http://www.url.com`

### Legal citations

- Italicize court-case names in text.
- Supreme Court: `Olmstead v. United States, U.S. Reports, vol. 277, 1928, p. 438.`
- Lower court: reporter series, volume, year, page, court in parentheses.
- Laws: `U.S. Code, Title 18, section 3123(a)(1),(2), 2000 and 2002 Supplement.` or Public Law
  number, sections, U.S. Statutes at Large volume, year, page.

### News articles

- Print: `J. K. Author, "Title of the article," Title of the News Source, Month, Day, Year.`
- Online: append `[Online]. Available: http://www.url.com`

### Online video

- `Video Owner/Creator, Location (if available). Title of Video: In Initial Caps. (Release
  date). Accessed: Month Day, Year. [Online Video]. Available: URL`

### Patents

- `J. K. Author, "Title of patent," U.S. Patent x xxx xxx, Abbrev. Month, day, year.` or
  `... Country Patent xxx, ...` Retain or request the day of the month; use the issued date if
  several dates are given.
- Online: `Name of the invention, by inventor's name. (year, month day). Patent Number
  [Type of medium]. Available: site/path/file`

### Reports

- `J. K. Author, "Title of report," Abbrev. Name of Co., City of Co., Abbrev. State, Country,
  Rep. xxx, year.` (Report number and date at the end.)
- Online: `J. K. Author, "Title of report," Company, City, State, Country, Rep. no., (optional:
  vol./issue), Date. Accessed: Date. [Online]. Available: site/path/file` — ensure a year is
  included.

### Software

- `J. K. Author. Title of Software. (Date). Repository or Archive. (version or year). Publisher
  Name. Accessed: Date (when applicable). [Type of Medium]. Global Persistent Identifier.
  Available: site/path/file`
- IEEE follows the FORCE11 Software Citation Principles: importance (software is a legitimate,
  citable research product, included in the reference list, not omitted or separated), credit
  and attribution, unique identification (machine-actionable, globally unique, interoperable
  identifier), persistence, accessibility, and specificity (identify the exact version, revision,
  or platform variant used).

### Standards

- `Title of Standard, Standard number, Corporate author, location, date.` or
  `Title of Standard, Standard number, date.`
- Online: append `[Online]. Available: http://www.url.com`

### Theses and dissertations

- `J. K. Author, "Title of thesis," M.S. thesis, Abbrev. Dept., Abbrev. Univ., City of Univ.,
  Abbrev. State, year.`
- `J. K. Author, "Title of dissertation," Ph.D. dissertation, Abbrev. Dept., Abbrev. Univ.,
  City of Univ., Abbrev. State, year.`
- Online: append `[Online]. Available: http://www.url.com`
- Defer to the "thesis"/"dissertation" wording provided by the authors; these differ by degree
  and institution and should not be changed based on degree level. The state abbreviation is
  omitted if the university name includes the state name ("Univ. California, Berkeley").

### U.S. government documents

- `Legislative body. Number of Congress, Session. (year, month day). Number of bill or
  resolution, Title. [Type of medium]. Available: site/path/file`

### Unpublished and preprints

- Private communication: `J. K. Author, private communication, Abbrev. Month, year.`
- Paper in preparation: `J. K. Author, "Title of paper," unpublished.`
- arXiv preprint: `J. K. Author, "Title of paper," year, arXiv number.`

### Websites

- `First Name Initial(s) Last Name. "Page Title." Website Title. Date Accessed. [Online].
  Available: Web Address.`
- Omit titles and affiliations associated with the author; no comma before a suffix (Jr./Sr.,
  roman numeral). For two or more authors, list them in the order shown on the website,
  separated by commas. Social media posts follow the same style with the platform as website
  title.

### Blogs

- `J. K. Author, "Title of the post," Title of the Blog, Month, Day, Year. [Online]. Available:
  http://www.url.com`

## Notes about online references

- Accessed-date style: `Accessed: Abbrev. month and day, year.` Its placement within the
  reference should match the final author-submitted version. URLs are not hyperlinked in the
  proof.
- Ordering and final punctuation options: `Accessed date. DOI. [Online]. Available: URL` (no
  period at end); `Accessed date. [Online]. Available: URL` (no period at end); `Accessed date.
  DOI.` (period at end); `DOI. URL` (no period at end); `(no accessed date), DOI.` (period
  unless URL); `URL` (no period at end).
- Breaking URLs: break after a slash, double slash, or period; break *before* a hyphen that is
  part of an address, but not after; break before a tilde, hyphen, underscore, question mark, or
  percent symbol; break before or after an equal sign, ampersand, or at sign; do not add hyphens
  or spaces, and do not let addresses hyphenate.

## Abbreviating periodical titles

- Words ending in "-ology" can be ended after the "-ol." (Endocrinology → Endocrinol.).
- Words ending in "-graphy" can be ended after the "-gr." (Oceanography → Oceanogr.).
- Compound words can be ended using the abbreviation of the last word (Bioengineering →
  Bioeng.; Nanobioscience → Nanobiosci.).
- Some abbreviations cover more than one word ("Mathematical"/"Mathematics" → Math.;
  "Medical"/"Medicine" → Med.).
- If a word is not in the list and cannot be abbreviated by these rules, spell it out.

## Common abbreviations of words in references

| Word | Abbreviation |
| --- | --- |
| Abstracts | Abstr. |
| Academy | Acad. |
| Accelerator | Accel. |
| Acoustics | Acoust. |
| Active | Act. |
| Administration | Admin. |
| Administrative | Administ. |
| Advanced | Adv. |
| Aeronautics | Aeronaut. |
| Aerospace | Aerosp. |
| Affective | Affect. |
| Africa, African | Afr. |
| Aircraft | Aircr. |
| Algebraic | Algebr. |
| American | Amer. |
| Analysis | Anal. |
| Annals | Ann. |
| Annual | Annu. |
| Apparatus | App. |
| Applications | Appl. |
| Applied | Appl. |
| Approximate | Approx. |
| Architecture | Archit. |
| Archive(s) | Arch. |
| Article | Art. |
| Artificial | Artif. |
| Assembly | Assem. |
| Association | Assoc. |
| Astronomy | Astron. |
| Astronautics | Astronaut. |
| Astrophysics | Astrophys. |
| Atmosphere | Atmos. |
| Atomic, Atoms | At. |
| Australasian | Australas. |
| Australia | Aust. |
| Automatic | Autom. |
| Automation | Automat. |
| Automotive | Automot. |
| Autonomous | Auton. |
| Behavior(al) | Behav. |
| Belgian | Belg. |
| Biochemical | Biochem. |
| Bioinformatics | Bioinf. |
| Biology, Biological | Biol. |
| Biomedical | Biomed. |
| Biophysics | Biophys. |
| British | Brit. |
| Broadcasting | Broadcast. |
| Bulletin | Bull. |
| Bureau | Bur. |
| Business | Bus. |
| Canadian | Can. |
| Ceramic | Ceram. |
| Chemical | Chem. |
| Chinese | Chin. |
| Climatology | Climatol. |
| Clinical | Clin. |
| Cognitive | Cogn. |
| Colloquium | Colloq. |
| Communications | Commun. |
| Company | Co. |
| Compatibility | Compat. |
| Component(s) | Compon. |
| Computational | Comput. |
| Computer(s) | Comput. |
| Computing | Comput. |
| Condensed | Condens. |
| Conference | Conf. |
| Congress | Congr. |
| Consumer | Consum. |
| Conversion | Convers. |
| Convention | Conv. |
| Correspondence | Corresp. |
| Critical | Crit. |
| Crystal | Cryst. |
| Crystallography | Crystallogr. |
| Cybernetics | Cybern. |
| Decision | Decis. |
| Delivery | Del. |
| Department | Dept. |
| Design | Des. |
| Detector | Detect. |
| Development(al) | Develop. |
| Differential | Differ. |
| Digest | Dig. |
| Digital | Digit. |
| Disclosure | Discl. |
| Discussions | Discuss. |
| Dissertations | Diss. |
| Distributed | Distrib. |
| Dynamics | Dyn. |
| Earthquake | Earthq. |
| Economic(s) | Econ. |
| Edition | Ed. |
| Education | Educ. |
| Electrical | Elect. |
| Electrification | Electrific. |
| Electromagnetic | Electromagn. |
| Electroacoustic | Electroacoust. |
| Electronic | Electron. |
| Emerging | Emerg. |
| Engineering | Eng. |
| Environment | Environ. |
| Equations | Equ. |
| Equipment | Equip. |
| Ergonomics | Ergonom. |
| European | Eur. |
| Evaluation | Eval. |
| Evolutionary | Evol. |
| Exhibition | Exhib. |
| Experimental | Exp. |
| Exploratory | Explor. |
| Exposition | Expo. |
| Express | Exp. |
| Fabrication | Fabr. |
| Faculty | Fac. |
| Ferroelectrics | Ferroelect. |
| Francais, French | Fr. |
| Frequency | Freq. |
| Foundation | Found. |
| Fundamental | Fundam. |
| Generation | Gener. |
| Geology | Geol. |
| Geophysics | Geophys. |
| Geoscience | Geosci. |
| Graphics | Graph. |
| Guidance | Guid. |
| Harmonic(s) | Harmon. |
| History | Hist. |
| Horizon | Horiz. |
| Hungary, Hungarian | Hung. |
| Hydraulics | Hydraul. |
| Hydrology | Hydrol. |
| Illuminating | Illum. |
| Imaging | Imag. |
| Industrial | Ind. |
| Information | Inf. |
| Informatics | Inform. |
| Innovation | Innov. |
| Institute | Inst. |
| Instrument | Instrum. |
| Instrumentation | Instrum. |
| Insulation | Insul. |
| Integrated | Integr. |
| Intelligence | Intell. |
| Intelligent | Intell. |
| Interactions | Interact. |
| International | Int. |
| Isotopes | Isot. |
| Israel | Isr. |
| Japan | Jpn. |
| Journal | J. |
| Knowledge | Knowl. |
| Laboratory(ies) | Lab. |
| Language | Lang. |
| Learning | Learn. |
| Letter(s) | Lett. |
| Lightwave | Lightw. |
| Logic, Logical | Log. |
| Luminescence | Lumin. |
| Machine | Mach. |
| Magazine | Mag. |
| Magnetics | Magn. |
| Management | Manage. |
| Managing | Manag. |
| Manufacturing | Manuf. |
| Marine | Mar. |
| Material | Mater. |
| Mathematical | Math. |
| Mathematics | Math. |
| Measurement | Meas. |
| Mechanical | Mech. |
| Medical, Medicine | Med. |
| Metals | Met. |
| Metallurgy | Metall. |
| Meteorology | Meteorol. |
| Metropolitan | Metrop. |
| Mexican, Mexico | Mex. |
| Microelectromechanical | Microelectromech. |
| Microgravity | Microgr. |
| Microscopy | Microsc. |
| Microwave(s) | Microw. |
| Military | Mil. |
| Modeling | Model. |
| Molecular | Mol. |
| Monitoring | Monit. |
| Multiphysics | Multiphys. |
| Nanobioscience | Nanobiosci. |
| Nanotechnology | Nanotechnol. |
| National | Nat. |
| Naval | Nav. |
| Navigation | Navig. |
| Network, Networking | Netw. |
| Newsletter | Newslett. |
| Nondestructive | Nondestruct. |
| Nuclear | Nucl. |
| Numerical | Numer. |
| Observations | Observ. |
| Oceanic | Ocean. |
| Oceanography | Oceanogr. |
| Occupation | Occupat. |
| Operational | Oper. |
| Optical | Opt. |
| Optics | Opt. |
| Optimization | Optim. |
| Organization | Org. |
| Packaging | Packag. |
| Particle | Part. |
| Patent | Pat. |
| Performance | Perform. |
| Personal | Pers. |
| Philosophical | Philos. |
| Photonics | Photon. |
| Photovoltaics | Photovolt. |
| Physics | Phys. |
| Physiology | Physiol. |
| Planetary | Planet. |
| Pneumatics | Pneum. |
| Pollution | Pollut. |
| Polymer | Polym. |
| Polytechnic | Polytech. |
| Practice | Pract. |
| Precision | Precis. |
| Principles | Princ. |
| Proceedings | Proc. |
| Processing | Process. |
| Production | Prod. |
| Productivity | Productiv. |
| Programmable | Program. |
| Programming | Program. |
| Progress | Prog. |
| Propagation | Propag. |
| Psychology | Psychol. |
| Quality | Qual. |
| Quarterly | Quart. |
| Radiation | Radiat. |
| Radiology | Radiol. |
| Reactor | React. |
| Receivers | Receiv. |
| Recognition | Recognit. |
| Record | Rec. |
| Rehabilitation | Rehabil. |
| Reliability | Rel. |
| Report | Rep. |
| Research | Res. |
| Resonance | Reson. |
| Resources | Resour. |
| Review | Rev. |
| Robotics | Robot. |
| Royal | Roy. |
| Safety | Saf. |
| Satellite | Satell. |
| Scandinavian | Scand. |
| Science | Sci. |
| Section | Sect. |
| Security | Secur. |
| Seismology | Seismol. |
| Selected | Sel. |
| Semiconductor | Semicond. |
| Sensing | Sens. |
| Series | Ser. |
| Simulation | Simul. |
| Singapore | Singap. |
| Sistema | Sist. |
| Society | Soc. |
| Sociological | Sociol. |
| Software | Softw. |
| Solar | Sol. |
| Soviet | Sov. |
| Spectroscopy | Spectrosc. |
| Spectrum | Spectr. |
| Speculations | Specul. |
| Statistics | Statist. |
| Structure | Struct. |
| Studies | Stud. |
| Superconductivity | Supercond. |
| Supplement | Suppl. |
| Surface | Surf. |
| Survey | Surv. |
| Sustainable | Sustain. |
| Symposium | Symp. |
| Systems | Syst. |
| Technical | Tech. |
| Techniques | Techn. |
| Technology | Technol. |
| Telecommunications | Telecommun. |
| Television | Telev. |
| Temperature | Temp. |
| Terrestrial | Terr. |
| Theorem | Thm. |
| Theoretical | Theor. |
| Transactions | Trans. |
| Translation | Transl. |
| Transmission | Transmiss. |
| Transportation | Transp. |
| Tutorials | Tut. |
| Ultrasonic | Ultrason. |
| University | Univ. |
| Vacuum | Vac. |
| Vehicular | Veh. |
| Vibration | Vib. |
| Vision | Vis. |
| Visual | Vis. |
| Volume | Vol. |
| Welding | Weld. |
| Working | Work. |
