--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: available_dates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.available_dates (
    id integer NOT NULL,
    start_time character varying,
    end_time character varying,
    day character varying,
    doctor_id integer
);


ALTER TABLE public.available_dates OWNER TO postgres;

--
-- Name: available_dates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.available_dates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.available_dates_id_seq OWNER TO postgres;

--
-- Name: available_dates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.available_dates_id_seq OWNED BY public.available_dates.id;


--
-- Name: doctors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doctors (
    id integer NOT NULL,
    name character varying,
    email character varying,
    password character varying,
    phone character varying,
    clinic_location character varying,
    gender character varying,
    x_y character varying,
    about character varying,
    avatar character varying,
    dob date,
    spec_id integer
);


ALTER TABLE public.doctors OWNER TO postgres;

--
-- Name: doctors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.doctors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doctors_id_seq OWNER TO postgres;

--
-- Name: doctors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.doctors_id_seq OWNED BY public.doctors.id;


--
-- Name: favorites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favorites (
    patient_id integer NOT NULL,
    doctor_id integer NOT NULL,
    is_in_favorite_list boolean
);


ALTER TABLE public.favorites OWNER TO postgres;

--
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    seen boolean,
    "time" time without time zone,
    doctor_name character varying,
    patient_id integer
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notifications_id_seq OWNER TO postgres;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: patients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patients (
    id integer NOT NULL,
    name character varying,
    email character varying,
    password character varying,
    phone character varying,
    location character varying,
    gender character varying,
    about character varying,
    avatar character varying,
    dob date
);


ALTER TABLE public.patients OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.patients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.patients_id_seq OWNER TO postgres;

--
-- Name: patients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.patients_id_seq OWNED BY public.patients.id;


--
-- Name: periods; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.periods (
    id integer NOT NULL,
    "time" character varying,
    is_available boolean,
    available_date_id integer,
    session_id integer
);


ALTER TABLE public.periods OWNER TO postgres;

--
-- Name: periods_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.periods_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.periods_id_seq OWNER TO postgres;

--
-- Name: periods_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.periods_id_seq OWNED BY public.periods.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    patient_id integer,
    session_id integer NOT NULL,
    comment character varying,
    stars integer
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id integer NOT NULL,
    name character varying,
    gender character varying,
    date character varying,
    day character varying,
    "time" time without time zone,
    am_pm character varying(5),
    phone character varying,
    comment character varying,
    diagnosis character varying,
    medicines character varying,
    files character varying,
    patient_id integer,
    doctor_id integer
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sessions_id_seq OWNER TO postgres;

--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- Name: specializations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.specializations (
    id integer NOT NULL,
    name character varying,
    image character varying
);


ALTER TABLE public.specializations OWNER TO postgres;

--
-- Name: specializations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.specializations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.specializations_id_seq OWNER TO postgres;

--
-- Name: specializations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.specializations_id_seq OWNED BY public.specializations.id;


--
-- Name: available_dates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_dates ALTER COLUMN id SET DEFAULT nextval('public.available_dates_id_seq'::regclass);


--
-- Name: doctors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctors ALTER COLUMN id SET DEFAULT nextval('public.doctors_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: patients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients ALTER COLUMN id SET DEFAULT nextval('public.patients_id_seq'::regclass);


--
-- Name: periods id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.periods ALTER COLUMN id SET DEFAULT nextval('public.periods_id_seq'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- Name: specializations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specializations ALTER COLUMN id SET DEFAULT nextval('public.specializations_id_seq'::regclass);


--
-- Data for Name: available_dates; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.available_dates (id, start_time, end_time, day, doctor_id) FROM stdin;
1	04:00 pm	10:00 pm	Sunday	5
2	05:00 pm	10:00 pm	Tuesday	5
3	02:00 pm	6:00 pm	Monday	6
4	05:00 pm	10:00 pm	Saturday	4
5	02:00 pm	6:00 pm	Sunday	4
6	05:00 pm	09:00 pm	Wednesday	4
7	05:00 pm	10:00 pm	Thursday	3
8	05:00 pm	10:00 pm	Friday	3
9	06:00 pm	10:00 pm	Saturday	2
10	06:00 pm	10:00 pm	Monday	2
11	06:00 pm	10:00 pm	Wednesday	2
12	02:00 pm	5:00 pm	Friday	1
13	04:00 pm	11:00 pm	Sunday	1
\.


--
-- Data for Name: doctors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.doctors (id, name, email, password, phone, clinic_location, gender, about, avatar, dob, spec_id) FROM stdin;
1	Mohamed	mohamed@mail.com	sha256$VN65BHFe$3fb834ded588eb7af1d437d0b5f4359c034593a6ca7abc25271e8fec863fbcf4	8563415792	Egypt, Cairo, next to Cairo University	Male	Hello, there! I'm Dr.Mohamed 	default.png	1980-06-12	1
2	Ahmed	ahmed@mail.com	sha256$gIXiXltz$e74d4d8097ed2048875fe6ac2afbdbc5c2aa4d0faec1d012846394518b3bc88c	8563415792	Saudi Arabia	Male	Hey! I'm Dr.Ahmed. I'm a cardiologist 	default.png	1985-06-08	2
3	Peter	peter@mail.com	sha256$LK4WXfW9$4e481b2944af3a42f4aeb5548882182e989665a88ed874bb5274611058c33e38	54863258986	Egypt, Alexandria	Male	Hello! I'm Dr.Peter	default.png	1980-06-12	2
4	Osama	osama@mail.com	sha256$cAn5GwuU$7743409a673d4d40e6534981bd0907c42ccd768cac187baa6df78c4b3e65cd41	1245757575	Egypt	Male	Hi, I'm Dr.Osama 	default.png	1990-06-06	4
6	Jean	jean@mail.com	sha256$oCp7AriR$79cfbd4690c924e786821ac5d5c34b584084dd054ad08ba3e797e0c3dcdcf982	9865671545	USA	Female	I'm Dr.Jean	default.png	1995-06-12	1
5	Jessica	jessica@mail.com	sha256$PCOe7dDe$e63a0f85b0a600b70e7986722d723f41288befc53592d30119eb7d1948400111	589766512	USA	Female	I'm Dr.Jessica 	default.png	1980-06-12	5
\.


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favorites (patient_id, doctor_id, is_in_favorite_list) FROM stdin;
1	6	t
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, seen, "time", doctor_name, patient_id) FROM stdin;
1	t	15:30:00	Jean	1
2	f	06:14:00	Peter	1
3	t	08:00:00	Mohamed	2
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patients (id, name, email, password, phone, location, gender, about, avatar, dob) FROM stdin;
1	Alice	alice@mail.com	sha256$QGUZqBNJ$70fe533e7c44e0033eca6a0f0d9238ab08c577e32bcc0e80404de47f670d7683	12345678	USA	Male	Hey, I'm Alice from USA. I'm still young!! 	default.png	1995-09-09
2	William	william@mail.com	sha256$QRnPvXBs$6a126143ac1ff0a4e592a03b7798866854d90693495505f12d5951b1a79a2c37	8563415792	Canda	Male	Hello, there! I'm william, a new user in this app 	default.png	1999-03-15
4	John	john@mail.com	sha256$jBpws0YY$33a4efcc4f8012d43119461ba5430205ad1aaf6fc6e17156dae8b27af9a486eb	010111111111	Egypt	Male	Hello, I'm John	default.png	1885-12-20
3	Amy	amy@mail.com	sha256$20eMtakV$898d388aa72adf71e7aa0e0b17063ca11ed1bf54fc32cd0659373162c0118fb7	8563415792	UK	Female	Hey! I'm Amy	default.png	2000-03-15
\.


--
-- Data for Name: periods; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.periods (id, "time", is_available, available_date_id, session_id) FROM stdin;
1	04:00 pm	f	1	\N
2	04:30 pm	f	1	\N
3	05:00 pm	f	1	\N
4	05:30 pm	f	1	\N
5	06:00 pm	f	1	\N
6	06:30 pm	f	1	\N
7	07:00 pm	f	1	\N
9	08:00 pm	f	1	\N
10	08:30 pm	f	1	\N
11	09:00 pm	f	1	\N
12	09:30 pm	f	1	\N
13	05:00 pm	f	2	\N
14	05:30 pm	f	2	\N
15	06:00 pm	f	2	\N
16	06:30 pm	f	2	\N
17	07:00 pm	f	2	\N
18	07:30 pm	f	2	\N
19	08:00 pm	f	2	\N
20	08:30 pm	f	2	\N
21	09:00 pm	f	2	\N
22	09:30 pm	f	2	\N
23	02:00 pm	f	3	\N
26	03:30 pm	f	3	\N
27	04:00 pm	f	3	\N
28	04:30 pm	f	3	\N
29	05:00 pm	f	3	\N
30	05:30 pm	f	3	\N
31	05:00 pm	f	4	\N
32	05:30 pm	f	4	\N
33	06:00 pm	f	4	\N
34	06:30 pm	f	4	\N
35	07:00 pm	f	4	\N
36	07:30 pm	f	4	\N
37	08:00 pm	f	4	\N
38	08:30 pm	f	4	\N
39	09:00 pm	f	4	\N
40	09:30 pm	f	4	\N
41	02:00 pm	f	5	\N
42	02:30 pm	f	5	\N
43	03:00 pm	f	5	\N
44	03:30 pm	f	5	\N
46	04:30 pm	f	5	\N
47	05:00 pm	f	5	\N
48	05:30 pm	f	5	\N
49	05:00 pm	f	6	\N
50	05:30 pm	f	6	\N
51	06:00 pm	f	6	\N
52	06:30 pm	f	6	\N
53	07:00 pm	f	6	\N
54	07:30 pm	f	6	\N
55	08:00 pm	f	6	\N
56	08:30 pm	f	6	\N
57	05:00 pm	f	7	\N
58	05:30 pm	f	7	\N
59	06:00 pm	f	7	\N
60	06:30 pm	f	7	\N
61	07:00 pm	f	7	\N
62	07:30 pm	f	7	\N
63	08:00 pm	f	7	\N
64	08:30 pm	f	7	\N
65	09:00 pm	f	7	\N
66	09:30 pm	f	7	\N
67	05:00 pm	f	8	\N
68	05:30 pm	f	8	\N
69	06:00 pm	f	8	\N
70	06:30 pm	f	8	\N
71	07:00 pm	f	8	\N
72	07:30 pm	f	8	\N
73	08:00 pm	f	8	\N
74	08:30 pm	f	8	\N
75	09:00 pm	f	8	\N
76	09:30 pm	f	8	\N
77	06:00 pm	f	9	\N
78	06:30 pm	f	9	\N
79	07:00 pm	f	9	\N
80	07:30 pm	f	9	\N
81	08:00 pm	f	9	\N
82	08:30 pm	f	9	\N
83	09:00 pm	f	9	\N
84	09:30 pm	f	9	\N
85	06:00 pm	f	10	\N
86	06:30 pm	f	10	\N
87	07:00 pm	f	10	\N
88	07:30 pm	f	10	\N
89	08:00 pm	f	10	\N
90	08:30 pm	f	10	\N
91	09:00 pm	f	10	\N
92	09:30 pm	f	10	\N
93	06:00 pm	f	11	\N
94	06:30 pm	f	11	\N
97	08:00 pm	f	11	\N
98	08:30 pm	f	11	\N
99	09:00 pm	f	11	\N
100	09:30 pm	f	11	\N
101	02:00 pm	f	12	\N
102	02:30 pm	f	12	\N
103	03:00 pm	f	12	\N
104	03:30 pm	f	12	\N
105	04:00 pm	f	12	\N
106	04:30 pm	f	12	\N
107	04:00 pm	f	13	\N
108	04:30 pm	f	13	\N
109	05:00 pm	f	13	\N
110	05:30 pm	f	13	\N
111	06:00 pm	f	13	\N
112	06:30 pm	f	13	\N
113	07:00 pm	f	13	\N
114	07:30 pm	f	13	\N
116	08:30 pm	f	13	\N
117	09:00 pm	f	13	\N
118	09:30 pm	f	13	\N
119	10:00 pm	f	13	\N
120	10:30 pm	f	13	\N
24	02:30 pm	t	3	1
25	03:00 pm	f	3	\N
95	07:00 pm	t	11	3
96	07:30 pm	f	11	\N
8	07:30 pm	f	1	\N
45	04:00 pm	t	5	5
115	08:00 pm	t	13	6
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews (patient_id, session_id, comment, stars) FROM stdin;
1	2	The doctor was awesome	5
2	6	Good Doctor	4
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, name, gender, date, day, "time", am_pm, phone, comment, diagnosis, medicines, files, patient_id, doctor_id) FROM stdin;
1	Alice	Male	2021-04-19	Monday	02:30:00	pm	123659563	I suffer from a severe headache	\N	\N	\N	1	6
2	Alice	Male	2021-03-29	Monday	03:00:00	pm	123659563	I suffer from a severe headache	You are just exhausted	Take some aspirin	file1.jpg, file2.jpg	1	6
3	Alice	Male	2021-04-21	Wednesday	07:00:00	pm	123659563	I have a pain in my heart	\N	\N	\N	1	2
4	Alice	Male	2021-04-02	Friday	06:00:00	pm	123659563	my heart hurt	You are Great.	Take this medicine	file1.jpg	1	3
5	Willam	Male	2021-04-18	Sunday	04:00:00	pm	3648325635	I have a back pain	\N	\N	\N	2	5
6	William	Male	2021-04-04	Sunday	08:00:00	pm	123659563	I have a headache	Your are OK	You don't need any medicines	\N	2	1
\.


--
-- Data for Name: specializations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.specializations (id, name, image) FROM stdin;
1	Brain	https://cdn.pixabay.com/photo/2016/11/21/15/28/brain-1845962_1280.jpg
2	Heart	https://cdn.pixabay.com/photo/2013/07/18/10/59/pulse-trace-163708_1280.jpg
3	Dermatology	https://cdn.pixabay.com/photo/2019/06/06/00/30/acne-4254911_1280.png
4	Teeth	https://cdn.pixabay.com/photo/2016/09/14/20/50/teeth-1670434_960_720.png
5	Bone	https://cdn.pixabay.com/photo/2017/11/08/17/09/ribs-front-2931058_960_720.png
6	Physical	https://cdn.pixabay.com/photo/2016/04/01/09/23/abstract-1299334_1280.png
7	Urology	https://biomerics.com/wp-content/uploads/urology.jpg
8	Surgery	https://cdn.pixabay.com/photo/2017/01/31/22/23/blade-2027703_1280.png
9	Kids	https://thumbs.dreamstime.com/b/baby-face-icon-vector-illustration-design-template-172987114.jpg
10	Internal Medicine	https://cdn.pixabay.com/photo/2016/09/28/12/59/human-heart-1700453_960_720.png
11	Chest	https://cdn.pixabay.com/photo/2016/06/24/03/53/diagnosis-1476620_1280.jpg
\.


--
-- Name: available_dates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.available_dates_id_seq', 13, true);


--
-- Name: doctors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.doctors_id_seq', 6, true);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_id_seq', 3, true);


--
-- Name: patients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.patients_id_seq', 4, true);


--
-- Name: periods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.periods_id_seq', 120, true);


--
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_id_seq', 6, true);


--
-- Name: specializations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.specializations_id_seq', 11, true);


--
-- Name: available_dates available_dates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_dates
    ADD CONSTRAINT available_dates_pkey PRIMARY KEY (id);


--
-- Name: doctors doctors_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_email_key UNIQUE (email);


--
-- Name: doctors doctors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_pkey PRIMARY KEY (id);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (patient_id, doctor_id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: patients patients_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_email_key UNIQUE (email);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (id);


--
-- Name: periods periods_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.periods
    ADD CONSTRAINT periods_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (session_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: specializations specializations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.specializations
    ADD CONSTRAINT specializations_pkey PRIMARY KEY (id);


--
-- Name: available_dates available_dates_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.available_dates
    ADD CONSTRAINT available_dates_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id) ON DELETE CASCADE;


--
-- Name: doctors doctors_spec_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_spec_id_fkey FOREIGN KEY (spec_id) REFERENCES public.specializations(id) ON DELETE CASCADE;


--
-- Name: favorites favorites_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id) ON DELETE CASCADE;


--
-- Name: favorites favorites_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id) ON DELETE CASCADE;


--
-- Name: notifications notifications_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id) ON DELETE CASCADE;


--
-- Name: periods periods_available_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.periods
    ADD CONSTRAINT periods_available_date_id_fkey FOREIGN KEY (available_date_id) REFERENCES public.available_dates(id) ON DELETE CASCADE;


--
-- Name: periods periods_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.periods
    ADD CONSTRAINT periods_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON DELETE SET NULL;


--
-- Name: reviews reviews_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id) ON DELETE CASCADE;


--
-- Name: reviews reviews_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(id) ON DELETE CASCADE;


--
-- Name: sessions sessions_patient_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES public.patients(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

