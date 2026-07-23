-- Genesys Health — Supabase schema
-- Safe to run as many times as you like. It will not error if things already exist.
-- Supabase Dashboard → SQL Editor → New query → paste → Run.

-- 1. DEMO REQUESTS / CONTACT FORM ------------------------------------------
create table if not exists public.leads (
  id            uuid primary key default gen_random_uuid(),
  created_at    timestamptz not null default now(),
  full_name     text not null,
  email         text not null,
  phone         text,
  facility_name text,
  facility_type text,
  beds_sites    text,
  product       text,
  message       text,
  source_page   text,
  locale        text default 'en'
);
alter table public.leads enable row level security;
drop policy if exists "anon can insert leads" on public.leads;
create policy "anon can insert leads" on public.leads
  for insert to anon with check (true);

-- 2. CHAT MESSAGES ---------------------------------------------------------
create table if not exists public.chat_messages (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  session_id  text not null,
  sender      text not null check (sender in ('visitor','genesys')),
  body        text not null,
  contact     text,
  source_page text
);
alter table public.chat_messages enable row level security;
drop policy if exists "anon can insert chat" on public.chat_messages;
create policy "anon can insert chat" on public.chat_messages
  for insert to anon with check (true);

-- 3. NEWSLETTER ------------------------------------------------------------
create table if not exists public.subscribers (
  id         uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  email      text not null unique
);
alter table public.subscribers enable row level security;
drop policy if exists "anon can subscribe" on public.subscribers;
create policy "anon can subscribe" on public.subscribers
  for insert to anon with check (true);

-- 4. INDUSTRY NEWS ---------------------------------------------------------
create table if not exists public.news_items (
  id         uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  published  boolean not null default true,
  sort_order int not null default 0,
  source     text not null,
  dateline   text,
  title      text not null,
  summary    text not null,
  url        text not null
);
alter table public.news_items enable row level security;
drop policy if exists "anyone can read published news" on public.news_items;
create policy "anyone can read published news" on public.news_items
  for select to anon using (published = true);

-- 5. STORIES BY GENESYS ----------------------------------------------------
create table if not exists public.stories (
  id         uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  published  boolean not null default false,
  slug       text not null unique,
  kind       text,
  title      text not null,
  dek        text,
  body_md    text,
  read_mins  int default 7
);
alter table public.stories enable row level security;
drop policy if exists "anyone can read published stories" on public.stories;
create policy "anyone can read published stories" on public.stories
  for select to anon using (published = true);

-- 6. TESTIMONIALS ----------------------------------------------------------
create table if not exists public.testimonials (
  id         uuid primary key default gen_random_uuid(),
  published  boolean not null default false,
  quote      text not null,
  person     text,
  role_title text,
  facility   text,
  sort_order int default 0
);
alter table public.testimonials enable row level security;
drop policy if exists "anyone can read published testimonials" on public.testimonials;
create policy "anyone can read published testimonials" on public.testimonials
  for select to anon using (published = true);

-- DONE. If this ran without a red error, your database is ready.
-- Check: Table Editor (left sidebar) should list leads, chat_messages,
-- subscribers, news_items, stories and testimonials.
