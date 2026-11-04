# What Composio has for each platform

Checked 2026-11-04 with Composio's own tool search (`COMPOSIO_SEARCH_TOOLS` and `COMPOSIO_GET_TOOL_SCHEMAS`, read only). Labels:
- **VERIFIED live**: a real pull worked on a real account.
- **VERIFIED in the tool list**: the tool and its fields exist in Composio's list on that date. Not yet run on a real account, so it may still refuse or come back empty.
- **UNVERIFIED**: not checked, or not found.

"Not found" only ever means "not found in Composio's tool list on 2026-11-04". It never means the platform can't do it. Composio adds tools often: search again before telling the owner something is missing.

## Instagram: full breakdown

- **VERIFIED live** (the recipe ran on real accounts when the dashboard page was built, 2026; not re-run on 2026-11-04): the whole recipe in `full-breakdown.md` (`INSTAGRAM_GET_USER_INFO`, `INSTAGRAM_GET_USER_INSIGHTS` for 28 and 7 days with the follow_type breakdowns, daily new followers, online followers, demographics, `INSTAGRAM_GET_IG_USER_MEDIA`, `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` per reel incl. skip rate).
- Needs a Business or Creator account. Under 1,000 followers reel insights may be refused; under 100, audience numbers are hidden.
- **VERIFIED in the tool list, not used yet:** the media list also offers `view_count`, `shares_count`, `saved_count` fields, and media insights list `profile_activity` (feed posts) and `follows`, `profile_visits`, `link_clicks` (stories only). Photo and carousel insights exist in the same tool but the dashboard reads reels only.

## TikTok: not supported yet, use the weekly report route

- **VERIFIED in the tool list:** `TIKTOK_GET_USER_STATS` (follower_count, following_count, likes_count, video_count for the signed-in account; "stats may be delayed"), `TIKTOK_LIST_VIDEOS` (the owner's own **public** videos, newest first, 20 per page with a cursor; fields include view_count, like_count, comment_count, share_count, duration, create_time, title), `TIKTOK_QUERY_VIDEOS` (up to 20 known video IDs).
- **Not found in the tool list on 2026-11-04:** profile visits, follows per video, watch time, traffic source, audience. So a TikTok pull could give per video views, likes, comments and shares, enough for the normal and each score, but not a funnel.
- Until a live pull is checked: TikTok numbers come from an Analytics export or screenshots (weekly report). If the owner wants to try it, it's read only and safe; save it as `my-content-team/analytics/{date}-tiktok.json` and score it with the weekly report rules, never on the Instagram page.

## Facebook Pages: not supported yet

- **VERIFIED in the tool list:** `FACEBOOK_LIST_MANAGED_PAGES`, `FACEBOOK_GET_PAGE_INSIGHTS` (page_follows, page_daily_follows_unique, page_daily_unfollows_unique, page_media_view, page_post_engagements, page_video_views, page_total_actions; up to 90 days), `FACEBOOK_GET_PAGE_POSTS` (posts with reactions, comments and shares counts via `.summary(true)`), `FACEBOOK_GET_POST_INSIGHTS` (post_media_view and post_total_media_view_unique only; Composio's note says the older per post metrics were removed by Facebook on 2025-11-15).
- Pages only, not personal profiles.
- Until a live pull is checked: Facebook export (Meta Business Suite) or screenshots, weekly report route.

## YouTube: not supported yet

- **VERIFIED in the tool list:** `YOUTUBE_LIST_CHANNELS` / `YOUTUBE_GET_CHANNEL_STATISTICS` (subscribers, views, video count; `mine: true`), `YOUTUBE_LIST_CHANNEL_VIDEOS` (`mine: true`), `YOUTUBE_GET_VIDEO_DETAILS_BATCH` (statistics per video, 50 at a time), `YOUTUBE_QUERY_ANALYTICS` (YouTube Analytics reports for `channel==MINE`: metrics and dimensions such as views by day; which metrics work is up to YouTube's Analytics API).
- This is the richest of the other platforms, but none of it has been run for a team pull yet.
- Until then: YouTube Studio export or screenshots, weekly report route.

## LinkedIn: company pages only, not supported yet

- **VERIFIED in the tool list:** `LINKEDIN_GET_SHARE_STATS` and `LINKEDIN_ADS_GET_ORG_SHARE_STATISTICS` (impressions, clicks, likes, comments, shares for an organization's posts), `LINKEDIN_GET_ORG_PAGE_STATS` (page views), `LINKEDIN_ADS_GET_ORG_FOLLOWER_STATISTICS` and `LINKEDIN_GET_NETWORK_SIZE` (followers). All need an organization (company page) the owner is an admin of.
- **Not found in the tool list on 2026-11-04:** statistics for a personal LinkedIn profile's posts.
- Until a live pull is checked: LinkedIn's own analytics export or screenshots, weekly report route.

## Before you build anything on these

Run one live read only pull on a real account, note what came back (and what came back empty) here with the date, then move the platform up from "in the tool list" to "live". Never tell the owner a platform "can't" give a number: say "Composio didn't have that when we last checked ({date})".
