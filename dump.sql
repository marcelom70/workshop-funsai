--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.13 (Debian 15.13-1.pgdg120+1)

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
-- Name: pessoas; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.pessoas (
    id integer NOT NULL,
    nome character varying NOT NULL,
    profissao character varying NOT NULL,
    idade integer NOT NULL,
    hobby character varying
);


ALTER TABLE public.pessoas OWNER TO "user";

--
-- Name: pessoas_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.pessoas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pessoas_id_seq OWNER TO "user";

--
-- Name: pessoas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.pessoas_id_seq OWNED BY public.pessoas.id;


--
-- Name: pessoas id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.pessoas ALTER COLUMN id SET DEFAULT nextval('public.pessoas_id_seq'::regclass);


--
-- Data for Name: pessoas; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.pessoas (id, nome, profissao, idade, hobby) FROM stdin;
1	João Silva	jornalista	40	viajar
2	Sérgio Noronha	educador	60	jogar bola
3	Carla Santana	repórter	28	academia
\.


--
-- Name: pessoas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.pessoas_id_seq', 3, true);


--
-- Name: pessoas pessoas_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.pessoas
    ADD CONSTRAINT pessoas_pkey PRIMARY KEY (id);


--
-- Name: ix_pessoas_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX ix_pessoas_id ON public.pessoas USING btree (id);


--
-- PostgreSQL database dump complete
--

