# Magic Friendz Tracker

Multiplayer MTG playgroup stats (Elo, matches, commanders) with Firebase Auth and Firestore.

## Live app (use this URL)

**Production:** [https://magic-friends-tracker.netlify.app/index.html](https://magic-friends-tracker.netlify.app/index.html)

Share your group with:

```text
https://magic-friends-tracker.netlify.app/index.html?group=YOUR_GROUP_SLUG
```

`YOUR_GROUP_SLUG` is the **document id** in Firestore → `groups` (e.g. `magic-friendz`). It is created when you name the group (lowercase, hyphens). Typos in the URL cause “Group Not Found”.

Also deployed on GitHub Pages; use **one** host consistently for magic links (see [FIREBASE_SETUP.md](FIREBASE_SETUP.md)).

## Backoffice

[admin.html](admin.html) on the same host (`/admin.html` or `/admin` after deploy) — set `admins/{uid}` in Firestore and sign in with Firebase email/password.

Local dev: `python3 -m http.server 3000` then open `http://localhost:3000/admin.html` (or `http://localhost:3000/admin/`).

## Local / setup

1. Open `index.html` via a local server (not `file://`) if testing auth.
2. Follow [FIREBASE_SETUP.md](FIREBASE_SETUP.md) for Auth, rules, and domains.

## Main files

| File | Purpose |
|------|---------|
| `index.html` | Player app |
| `admin.html` | Global admin |
| `firestore.rules` | Security rules |
