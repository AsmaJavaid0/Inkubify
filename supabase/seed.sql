-- seed.sql
-- Phase 1: Active skills catalog

insert into public.skills (slug, name, category, sort_order, is_active)
values
  -- Marketing & Sales
  ('digital-marketing', 'Digital Marketing', 'Marketing & Sales', 10, true),
  ('meta-ads', 'Meta (Facebook/Instagram) Ads', 'Marketing & Sales', 20, true),
  ('social-media', 'Social Media Management', 'Marketing & Sales', 30, true),
  ('seo', 'SEO', 'Marketing & Sales', 40, true),
  ('sales', 'Sales & Negotiation', 'Marketing & Sales', 50, true),
  ('content-writing', 'Content Writing', 'Marketing & Sales', 60, true),
  ('copywriting', 'Copywriting', 'Marketing & Sales', 70, true),

  -- Creative
  ('graphic-design', 'Graphic Design', 'Creative', 110, true),
  ('ui-ux-design', 'UI/UX Design', 'Creative', 120, true),
  ('photo-video', 'Photography & Video', 'Creative', 130, true),
  ('branding', 'Branding', 'Creative', 140, true),

  -- Technology
  ('web-dev', 'Web Development', 'Technology', 210, true),
  ('mobile-dev', 'Mobile App Development', 'Technology', 220, true),
  ('ai-data', 'AI & Data', 'Technology', 230, true),
  ('no-code', 'No-code Tools', 'Technology', 240, true),
  ('ecommerce-platforms', 'E-commerce Platforms (Shopify/WooCommerce/Daraz seller tools)', 'Technology', 250, true),

  -- Operations & Finance
  ('operations', 'Operations & Logistics', 'Operations & Finance', 310, true),
  ('supply-chain', 'Sourcing & Supply Chain', 'Operations & Finance', 320, true),
  ('finance', 'Accounting & Finance', 'Operations & Finance', 330, true),
  ('project-mgmt', 'Project Management', 'Operations & Finance', 340, true),
  ('customer-support', 'Customer Support', 'Operations & Finance', 350, true),
  ('legal-compliance', 'Registration & Compliance Basics', 'Operations & Finance', 360, true)
on conflict (slug) do update
set
  name = excluded.name,
  category = excluded.category,
  sort_order = excluded.sort_order,
  is_active = excluded.is_active;
