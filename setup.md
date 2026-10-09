# Setup Guide

This guide explains how to configure your Gemini API key and set up Google Sheets and Gmail API credentials for this project.

## 1. Get your Gemini API key

1. Open the official Google AI Studio API key page: https://aistudio.google.com/apikey
2. Sign in with your Google account.
3. Click **Create API key**.
4. Select an existing Google Cloud project or create a new one if prompted.
5. Copy the generated API key.

If you've already created a key, it should appear on this page, where you can manage your existing keys.

Official documentation: https://ai.google.dev/gemini-api/docs/api-key

### Add the Gemini API key to `.env`

From the project root, create a `.env` file from the example file if one exists:

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with your real key. For example:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

Keep `.env` out of Git. Add the following entry to `.gitignore` if it is not already present:

```gitignore
.env
```

Do not commit or share your real API key.

## 2. Create a Google Cloud project

1. Open Google Cloud Console: https://console.cloud.google.com/
2. Sign in with the Google account you want your application to use.
3. Click the project selector at the top.
4. Select **New Project**.
5. Enter a project name, such as `Sheets-Gmail-Integration`.
6. Leave Organization and Location at their defaults if you don't need to change them.
7. Click **Create**.
8. Wait for the project to be created, then select it from the project selector.

## 3. Enable the Google Sheets API

1. Open the Google Sheets API page: https://console.cloud.google.com/apis/library/sheets.googleapis.com
2. Confirm that your new project is selected at the top.
3. Click **Enable**.
4. If the page already says **Manage**, the API is enabled.

## 4. Enable the Gmail API

1. Open the Gmail API page: https://console.cloud.google.com/apis/library/gmail.googleapis.com
2. Confirm that the same project is selected.
3. Click **Enable**.

You should now have both APIs enabled.

## 5. Configure the Google OAuth consent screen

Your application needs permission to access Gmail and Google Sheets on your behalf.

1. Open Google Auth Platform: https://console.cloud.google.com/auth/overview
2. Make sure your project is selected.
3. If prompted to configure Google Auth, click **Get started**.
4. Under **App Information**:
   - App name: `My Sheets Gmail App`
   - User support email: select your email.
5. Click **Next**.
6. Under **Audience**, select **External** if you're using a personal Gmail account and the option is available.
7. Click **Next**.
8. Under **Contact Information**, enter your email address.
9. Agree to the applicable terms and click **Create**.

If your application is in testing mode:

1. Open **Google Auth Platform → Audience → Test users**.
2. Click **Add users**.
3. Enter your Gmail address.
4. Save the changes.

Official reference: https://developers.google.com/workspace/gmail/api/quickstart/python

## 6. Create and download `credentials.json`

These steps are for a local script or application that runs on your computer.

1. Open Google Auth Platform → Clients: https://console.cloud.google.com/auth/clients
2. Confirm that the correct project is selected.
3. Click **Create Client**.
4. For **Application type**, select **Desktop app**.
5. Name it `Local Sheets Gmail App`.
6. Click **Create**.
7. Once the client is created, download its JSON file. Depending on the interface, you may first need to close the creation dialog and select the download icon beside your client.
8. The downloaded file will usually have a name similar to `client_secret_123456789-abcdef.apps.googleusercontent.com.json`.
9. Rename it to exactly `credentials.json`.

**Important:** For a deployed web application, you generally need a **Web application** OAuth client with the appropriate redirect URIs instead of a Desktop app client.

Official reference: https://developers.google.com/workspace/guides/create-credentials

## 7. Move `credentials.json` into the project root

For example, your project might look like this:

```text
my-project/
├── main.py
├── credentials.json
├── .env
└── .gitignore
```

On a Mac:

1. Open your project in VS Code.
2. In the VS Code menu, select **Terminal → New Terminal**.
3. Run `pwd` to check that the terminal is in the project root.
4. If the downloaded JSON file is in your Downloads folder and there is only one matching file, run:

   ```bash
   mv ~/Downloads/client_secret_*.json ./credentials.json
   ```

   If the command reports an error, move the file using Finder instead.

5. Verify that the file is present:

   ```bash
   ls -l credentials.json
   ```

## 8. Protect your credentials

Add these entries to your project's `.gitignore` file:

```gitignore
.env
credentials.json
token.json
```

- `.env` contains your Gemini API key and possibly other secrets.
- `credentials.json` contains your OAuth client configuration.
- `token.json` is commonly created after your first successful Google sign-in and can contain access or refresh tokens.

Do not commit or share these files publicly.

## 9. Run your application

Once your code is configured to load `credentials.json`, run your project's normal startup command. For a Python project, that might be:

```bash
python3 main.py
```

The first run may open a browser window asking you to sign in to Google and authorize the requested Gmail and Sheets permissions. Follow the prompts.

**Note:** Enabling APIs and downloading `credentials.json` does not automatically grant access to Gmail or spreadsheets. Your application must implement OAuth authentication and request the required permissions.
