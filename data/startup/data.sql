
--
-- Data for Name: taxonomy_programtype; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_programtype (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
5	f	acceleration1	Acceleration	Acceleration	Acceleration	\N	\N	\N		\N		0
6	f	incubation1	Incubation	Incubation	Incubation	\N	\N	\N		\N		0
\.


--
-- Data for Name: taxonomy_typeofassistantship; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeofassistantship (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	funding	Funding	Funding	Funding		\N	\N		\N	\N	0
2	f	consumer-contact	Consumer contact	Consumer contact	Consumer contact		\N	\N		\N	\N	0
3	f	market-reach	Market Reach	Market Reach	Market Reach		\N	\N		\N	\N	0
4	f	law-and-regulation	Law and regulation	Law and regulation	Law and regulation		\N	\N		\N	\N	0
5	f	product-development	Product development	Product development	Product development		\N	\N		\N	\N	0
6	f	business-model-generation	Business model generation	Business model generation	Business model generation		\N	\N		\N	\N	0
7	f	technical-assistance	Technical assistance	Technical assistance	Technical assistance		\N	\N		\N	\N	0
8	f	accounting	Accounting	Accounting	Accounting		\N	\N		\N	\N	0
9	f	personnel	Personnel	Personnel	Personnel		\N	\N		\N	\N	0
10	f	pitching	Pitching	Pitching	Pitching		\N	\N		\N	\N	0
11	f	other	Other	Other	Other		\N	\N		\N	\N	0
\.


--
-- Data for Name: taxonomy_typeofattachment; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeofattachment (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority, attachment_for) FROM stdin;
2	f	summary-of-the-activities-of-the-program	Summary of the activities of the program	Summary of the activities of the program	Summary of the activities of the program		\N	\N		\N	\N	0	program
3	f	long-term-sustainable-revenue-model	Long-term sustainable revenue model	Long-term sustainable revenue model	Long-term sustainable revenue model		\N	\N		\N	\N	0	program
4	f	minimum-5-resumes-or-portfolio	Minimum 5 resumes or portfolio(consisting of previous achievement) of mentors, coaches, speaker, and trainers	Minimum 5 resumes or portfolio(consisting of previous achievement) of mentors, coaches, speaker, and trainers	Minimum 5 resumes or portfolio(consisting of previous achievement) of mentors, coaches, speaker, and trainers		\N	\N		\N	\N	0	program
5	f	program-plans-in-the-future	Program plans in the future	Program plans in the future	Program plans in the future		\N	\N		\N	\N	0	program
6	f	list-of-notable-startup-team-alumni	List of notable startup/team alumni	List of notable startup/team alumni	List of notable startup/team alumni		\N	\N		\N	\N	0	program
7	f	list-of-organization-or-program-partners	List of organization or program partners	List of organization or program partners	List of organization or program partners		\N	\N		\N	\N	0	program
9	f	incorporation-registration-certificate-startup	Incorporation/Registration Certificate	Incorporation/Registration Certificate	Incorporation/Registration Certificate		\N	\N		\N	\N	0	startup
10	f	minimum-5-biography	Minimum 5 biography consisting of major achievements (if any) of management levels	Minimum 5 biography consisting of major achievements (if any) of management levels	Minimum 5 biography consisting of major achievements (if any) of management levels		\N	\N		\N	\N	0	startup
11	f	list-of-partners	List of organizational or program partners (if any)	List of organizational or program partners (if any)	List of organizational or program partners (if any)		\N	\N		\N	\N	0	startup
12	f	other-start-up	Other	Other	Other		\N	\N		\N	\N	0	startup
8	f	other-program	Other	Other	Other		\N	\N		\N	\N	0	program
1	f	incorporation-registration-certificate-program	Incorporation/Registration Certificate	Incorporation/Registration Certificate	Incorporation/Registration Certificate		\N	\N		\N	\N	0	program
13	f	financial-statement	Financial Statement	Financial Statement	Financial Statement		\N	\N		\N	\N	0	investor
14	f	investment-portfolio	Investment Portfolio	Investment Portfolio	Investment Portfolio		\N	\N		\N	\N	0	investor
15	f	other-investor	Other	Other	Other		\N	\N		\N	\N	0	investor
\.


--
-- Data for Name: taxonomy_typeofbatch; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeofbatch (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	batch-1	batch-1	batch-1	batch-1		\N	\N		\N	\N	0
2	f	batch-2	batch-2	batch-2	batch-2		\N	\N		\N	\N	0
3	f	batch-3	batch-3	batch-3	batch-3		\N	\N		\N	\N	0
4	f	batch-4	batch-4	batch-4	batch-4		\N	\N		\N	\N	0
5	f	batch-5	batch-5	batch-5	batch-5		\N	\N		\N	\N	0
\.


--
-- Data for Name: taxonomy_typeoffinancialsource; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeoffinancialsource (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	fff	FFF(Personal connections such as friends and family)	FFF(Personal connections such as friends and family)	FFF(Personal connections such as friends and family)		\N	\N		\N	\N	0
2	f	program	Incubator/Accelerators	Incubator/Accelerators	Incubator/Accelerators		\N	\N		\N	\N	0
3	f	angels	Angels	Angels	Angels		\N	\N		\N	\N	0
4	f	venture-capital	Venture Capital	Venture Capital	Venture Capital		\N	\N		\N	\N	0
5	f	cooperated-venture-capital	Cooperated Venture Capital	Cooperated Venture Capital	Cooperated Venture Capital		\N	\N		\N	\N	0
6	f	other	Other	Other	Other		\N	\N		\N	\N	0
\.


--
-- Data for Name: taxonomy_typeoffocusindustry; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeoffocusindustry (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	next-generation-automotive	Next-Generation Automotive	Next-Generation Automotive	Next-Generation Automotive		\N	\N		\N	\N	0
2	f	smart-electronics	Smart Electronics	Smart Electronics	Smart Electronics		\N	\N		\N	\N	0
3	f	affluent-medical-and-wellness-tourism	Affluent, Medical and Wellness Tourism	Affluent, Medical and Wellness Tourism	Affluent, Medical and Wellness Tourism		\N	\N		\N	\N	0
4	f	agriculture-and-biotechnology	Agriculture and Biotechnology	Agriculture and Biotechnology	Agriculture and Biotechnology		\N	\N		\N	\N	0
5	f	food-for-the-future	Food for the Future	Food for the Future	Food for the Future		\N	\N		\N	\N	0
6	f	robotics	Robotics	Robotics	Robotics		\N	\N		\N	\N	0
7	f	aviation-and-logistics	Aviation and Logistics	Aviation and Logistics	Aviation and Logistics		\N	\N		\N	\N	0
8	f	biofuels-and-biochemicals	Biofuels and Biochemicals	Biofuels and Biochemicals	Biofuels and Biochemicals		\N	\N		\N	\N	0
9	f	digital	Digital	Digital	Digital		\N	\N		\N	\N	0
10	f	medical-hub	Medical Hub	Medical Hub	Medical Hub		\N	\N		\N	\N	0
11	f	other	Other	Other	Other		\N	\N		\N	\N	0
\.


--
-- Data for Name: taxonomy_typeoffocussector; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeoffocussector (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	health-tech	HealthTech	HealthTech	HealthTech	\N	\N	\N		\N		0
2	f	travel-tech	TravelTech	TravelTech	TravelTech	\N	\N	\N		\N		0
3	f	fin-tech	FinTech	FinTech	FinTech	\N	\N	\N		\N		0
4	f	business-service-tech	Business/ServicesTech	Business/ServicesTech	Business/ServicesTech	\N	\N	\N		\N		0
5	f	industry-tech	IndustryTech	IndustryTech	IndustryTech	\N	\N	\N		\N		0
6	f	property-urban-tech	Property/UrbanTech	Property/UrbanTech	Property/UrbanTech	\N	\N	\N		\N		0
7	f	gov-ed-tech	Gov/EdTech	Gov/EdTech	Gov/EdTech	\N	\N	\N		\N		0
8	f	lifestyle-tech	LifestyleTech	LifestyleTech	LifestyleTech	\N	\N	\N		\N		0
9	f	ag-tech-food-tech	AgTech/FoodTech	AgTech/FoodTech	AgTech/FoodTech	\N	\N	\N		\N		0
10	f	other	Other	Other	Other	\N	\N	\N		\N		0
\.


--
-- Data for Name: taxonomy_typeoffunding; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeoffunding (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	seed	Seed	Seed	Seed		\N	\N		\N	\N	0
2	f	series-a	Series A	Series A	Series A		\N	\N		\N	\N	0
3	f	series-b	Series B	Series B	Series B		\N	\N		\N	\N	0
4	f	series-c	Series C	Series C	Series C		\N	\N		\N	\N	0
5	f	series-d	Series D	Series D	Series D		\N	\N		\N	\N	0
6	f	series-e	Series E	Series E	Series E		\N	\N		\N	\N	0
7	f	series-f	Series F	Series F	Series F		\N	\N		\N	\N	0
8	f	series-g	Series G	Series G	Series G		\N	\N		\N	\N	0
9	f	series-h	Series H	Series H	Series H		\N	\N		\N	\N	0
10	f	series-i	Series I	Series I	Series I		\N	\N		\N	\N	0
11	f	series-j	Series J	Series J	Series J		\N	\N		\N	\N	0
12	f	venture-series unknown	Venture-Series Unknown	Venture-Series Unknown	Venture-Series Unknown		\N	\N		\N	\N	0
13	f	angel	Angel	Angel	Angel		\N	\N		\N	\N	0
14	f	private-equity	Private Equity	Private Equity	Private Equity		\N	\N		\N	\N	0
15	f	debt-financing	Debt Financing	Debt Financing	Debt Financing		\N	\N		\N	\N	0
16	f	convertible-note	Convertible Note	Convertible Note	Convertible Note		\N	\N		\N	\N	0
17	f	grant	Grant	Grant	Grant		\N	\N		\N	\N	0
18	f	corporate-round	Corporate Round	Corporate Round	Corporate Round		\N	\N		\N	\N	0
19	f	equity-crowdfunding	Equity Crowdfunding	Equity Crowdfunding	Equity Crowdfunding		\N	\N		\N	\N	0
20	f	product-crowdfunding	Product Crowdfunding	Product Crowdfunding	Product Crowdfunding		\N	\N		\N	\N	0
21	f	secondary-market	Secondary Market	Secondary Market	Secondary Market		\N	\N		\N	\N	0
22	f	post-ipo-equity	Post-IPO Equity	Post-IPO Equity	Post-IPO Equity		\N	\N		\N	\N	0
23	f	post-ipo-debt	Post-IPO Debt	Post-IPO Debt	Post-IPO Debt		\N	\N		\N	\N	0
24	f	post-ipo-secondary	Post-IPO Secondary	Post-IPO Secondary	Post-IPO Secondary		\N	\N		\N	\N	0
25	f	non-equity-assistance	Non-equity Assistance	Non-equity Assistance	Non-equity Assistance		\N	\N		\N	\N	0
26	f	initial-coin-offing	Initial Coin Offing	Initial Coin Offing	Initial Coin Offing		\N	\N		\N	\N	0
\.


--
-- Data for Name: taxonomy_typeofinvestmentstage; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeofinvestmentstage (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	pre-seed	Pre-seed	Pre-seed	Pre-seed		\N	\N		\N	\N	0
2	f	seed	Seed	Seed	Seed		\N	\N		\N	\N	0
3	f	pre-series-a	Pre-series A	Pre-series A	Pre-series A		\N	\N		\N	\N	0
4	f	series-a	Series A	Series A	Series A		\N	\N		\N	\N	0
5	f	series-b	Series B	Series B	Series B		\N	\N		\N	\N	0
6	f	series-c	Series C	Series C	Series C		\N	\N		\N	\N	0
\.

--
-- Data for Name: taxonomy_typeofstageofparticipant; Type: TABLE DATA; Schema: public; Owner: startup
--

COPY taxonomy_typeofstageofparticipant (id, is_deleted, permalink, title, title_th, title_en, summary, summary_th, summary_en, description, description_th, description_en, priority) FROM stdin;
1	f	idea	Idea	Idea	Idea		\N	\N		\N	\N	0
2	f	prototype	Prototype	Prototype	Prototype		\N	\N		\N	\N	0
3	f	launched	Launched	Launched	Launched		\N	\N		\N	\N	0
4	f	scaled-up	Scaled up	Scaled up	Scaled up		\N	\N		\N	\N	0
\.