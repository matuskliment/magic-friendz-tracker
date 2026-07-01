# Firebase setup (group auth)

Do these steps **after** deploying the latest `index.html` / `admin.html`.

## 1. Authentication

1. Firebase Console → **Authentication** → **Sign-in method**
2. Enable **Email/Password**
3. On the same provider, enable **Email link (passwordless sign-in)**
4. **Settings** → **Authorized domains** → add every host you use:
   - `localhost` (local testing only)
   - `edhstatstracker.xyz` (production)
   - `magic-friends-tracker.netlify.app` (Netlify deploy host, if still used)
   - `matuskliment.github.io` (GitHub Pages, optional)
   - Any other custom domain

Magic links only work on domains in this list.

## 2. Firestore rules

1. Firebase Console → **Firestore** → **Rules**
2. Copy contents of `firestore.rules` from this repo
3. Click **Publish**

Your existing data is **not** deleted when you publish rules.

If invites fail with **Missing or insufficient permissions**, publish the latest `firestore.rules` from this repo. Owners must be allowed to write `roster` and `memberEmails` even when `members/{uid}` was set up only on the group document.

## 3. Live app URL (share one host)

Use **one** URL for the playgroup day to day (bookmarks, invites, magic links):

**Recommended:** `https://edhstatstracker.xyz/?group=YOUR_GROUP_SLUG`

Replace `YOUR_GROUP_SLUG` with the Firestore document id under `groups/` (see README).

GitHub Pages (`https://matuskliment.github.io/magic-friendz-tracker/`) can stay enabled as a backup deploy. Do not mix hosts when sending and opening magic links on the same device.

## 4. Magic-link email copy (inbox)

Passwordless sign-in uses `sendSignInLinkToEmail`. Firebase sends that email from a **fixed default template**. It often says “Sign in to project-…” and includes a timestamp so Gmail does not hide the link in a thread.

**There is usually no “Email link sign-in” row** under Authentication → Templates (only verification, password reset, etc.). Editing “Email address verification” does **not** change magic-link sign-in emails.

What you can do:

| Approach | Effort |
|----------|--------|
| Set **Project settings → General → Public-facing name** to `Magic Friendz Tracker` | Low — may slightly improve wording |
| Rely on the **in-app** “Check your email” screen (after Send magic link) | Done in `index.html` |
| Custom email via **Cloud Function** + Admin SDK `generateSignInWithEmailLink` + SendGrid/Resend | High — full control of inbox copy |

For a small playgroup, the in-app message + spam hint is enough; inbox text stays generic unless you build custom mail.

## 5. Group owners (legacy / manual)

For each legacy group you should have:

- `groups/{groupId}` → `ownerUid`, `ownerEmail`
- `groups/{groupId}/members/{uid}` → `role: "owner"`, `email`, `joinedAt`

You can also set owners from **admin.html** → Selected Group → **Group owner**.

**Group slug:** the `?group=` value must match the Firestore document id exactly (e.g. `magic-friendz`, not a typo).

## 6. Global backoffice admin

- Firebase **Authentication** user (email/password) for you
- Firestore document: `admins/{your-uid}` (any fields)

## Roles (main app)

| Role | Can do |
|------|--------|
| Guest (group link only) | View stats, export JSON/CSV |
| Editor (signed in + invited) | Log matches, roster, invites |
| Owner | Editor + wipe match history |
| Backoffice admin | All groups, delete group/player, set owner |

## Smoke test (after deploy)

Use your real Netlify URL and Firestore group slug.

- [ ] Open `https://edhstatstracker.xyz/?group=SLUG` — dashboard loads (not “Group Not Found”)
- [ ] Guest: header/badge shows **View only**; cannot log a match
- [ ] Settings → Sign in → Send magic link → in-app **Check your email** appears
- [ ] Open link on **same device/browser** → signed in; badge **Owner** or **Can edit**
- [ ] Log a match; new player appears on roster as **Not invited**
- [ ] Invite player → inline “invite sent” (no need to read inbox wording)
- [ ] Sign out → confirmation → back to view-only
- [ ] Create group (optional): magic link → lands in new group as owner
