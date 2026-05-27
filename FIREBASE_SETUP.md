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

If invites fail with **Missing or insufficient permissions**, publish the latest `firestore.rules` from this repo. Owners must be allowed to write `roster` and `memberEmails` even when `members/{uid}` was set up only on the group document.

## 3. GitHub Pages URL

1. Repo **Settings** → **Pages** → deploy from branch **`main`**, folder **`/` (root)**
2. Note the live URL, e.g. `https://matuskliment.github.io/magic-friendz-tracker/`
3. Open the app at `.../index.html` and backoffice at `.../admin.html`

Magic-link sign-in only works on domains listed in Firebase (step 1).

## 4. Sign-in email copy (fix “project-822273509499”)

Firebase sends magic-link emails from the console template, **not** from `index.html`. Until you customize it, users see the generic “Sign in to project-…” message.

### 4a. Project display name

1. Firebase Console → **Project settings** (gear) → **General**
2. Set **Project name** and **Public-facing name** to: `Magic Friendz Tracker`
3. Save

This replaces `%APP_NAME%` in templates where Firebase uses it.

### 4b. Email link sign-in template

1. Firebase Console → **Authentication** → **Templates**
2. Open **Email link sign-in** (passwordless / email link flow)
3. Set **Sender name** to: `Magic Friendz Tracker`
4. Set **Subject** to something like:

   `Sign in to Magic Friendz Tracker`

5. Replace the **message body** with copy that matches the in-app flow. Example (Firebase inserts the link where you put `%LINK%`):

   ```text
   Hello,

   Use the link below to sign in to Magic Friendz Tracker with %EMAIL%.

   %LINK%

   Open the link on the same device and browser you used to request it. The link works once and expires after a short time.

   If you don’t see this message within a minute, check your spam folder.

   If you didn’t request this, you can ignore this email.

   — Magic Friendz Tracker
   ```

6. Click **Save**

**Note:** Exact placeholders depend on your Firebase console version. Common ones: `%LINK%`, `%EMAIL%`, `%APP_NAME%`. Use the **preview** in the template editor to confirm.

### 4c. Optional (later): custom domain / SMTP

For better deliverability and a `noreply@yourdomain.com` sender, use [Firebase Action URL customization](https://firebase.google.com/docs/auth/custom-email-handler) or a provider (SendGrid, Resend, etc.). Not required for a small group; customizing the template above is enough to fix the wording.

## 5. Group owners (already done manually)

For each legacy group you should have:

- `groups/{groupId}` → `ownerUid`, `ownerEmail`
- `groups/{groupId}/members/{uid}` → `role: "owner"`, `email`, `joinedAt`

You can also set owners from **admin.html** → Selected Group → **Group owner**.

## 6. Global backoffice admin

- Firebase **Authentication** user (email/password) for you
- Firestore document: `admins/{your-uid}` (any fields)

## Roles (main app)

| Role | Can do |
|------|--------|
| Guest (group name only) | View stats, export JSON/CSV |
| Editor (signed in + invited) | Log matches, roster, invites |
| Owner | Editor + wipe match history |
| Backoffice admin | All groups, delete group/player, set owner |
