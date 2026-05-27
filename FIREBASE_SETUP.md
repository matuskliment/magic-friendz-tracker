# Firebase setup (group auth)

Do these steps **after** deploying the latest `index.html` / `admin.html`.

## 1. Authentication

1. Firebase Console → **Authentication** → **Sign-in method**
2. Enable **Email/Password**
3. On the same provider, enable **Email link (passwordless)**
4. **Settings** → **Authorized domains** → add:
   - `localhost`
   - Your GitHub Pages host (e.g. `matuskliment.github.io`)
   - Any custom domain you use

## 2. Firestore rules

1. Firebase Console → **Firestore** → **Rules**
2. Copy contents of `firestore.rules` from this repo
3. Click **Publish**

Your existing data is **not** deleted when you publish rules.

## 3. GitHub Pages URL

1. Repo **Settings** → **Pages** → deploy from branch **`main`**, folder **`/` (root)**
2. Note the live URL, e.g. `https://matuskliment.github.io/magic-friendz-tracker/`
3. Open the app at `.../index.html` and backoffice at `.../admin.html`

Magic-link sign-in only works on domains listed in Firebase (step 1).

## 4. Group owners (already done manually)

For each legacy group you should have:

- `groups/{groupId}` → `ownerUid`, `ownerEmail`
- `groups/{groupId}/members/{uid}` → `role: "owner"`, `email`, `joinedAt`

You can also set owners from **admin.html** → Selected Group → **Group owner**.

## 5. Global backoffice admin

- Firebase **Authentication** user (email/password) for you
- Firestore document: `admins/{your-uid}` (any fields)

## Roles (main app)

| Role | Can do |
|------|--------|
| Guest (group name only) | View stats, export JSON/CSV |
| Editor (signed in + invited) | Log matches, roster, invites |
| Owner | Editor + wipe match history |
| Backoffice admin | All groups, delete group/player, set owner |
