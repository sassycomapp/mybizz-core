let's break the safe AI-assisted workflow into tiny, simple steps. Since you work only on Master now and want to try a dev branch per feature, we'll use that. No tech terms, just plain actions.

Step 1: Prep Your Branches
Open VSCode with your cloned Anvil repo.

Right-click Master branch (in bottom-left Git view), pick "Create new branch from...", name it "feature-login" (or whatever your first feature is).

Switch to this new dev branch—now your changes won't mess up Master.

Step 2: Build One Small Feature
Use GLM-5 in Continue.dev: Tell it one tiny job, like "Add a login button using my app specs."

Let it write just 10-20 lines of code—copy-paste into your Anvil files.

Save and test live via Anvil Uplink (run the server link to see it work).

Step 3: Polish and Check
Switch to Claude Sonnet 4.6 in Continue.dev: Say "Fix and polish this login code against my Anvil rules."

It tweaks the code—save again, test Uplink to confirm it works.

Run any simple checks you have (like Anvil's built-in tester) right away.

Step 4: Merge to Master (Your "PR")
PR means "Pull Request"—it's just a safe way to move code from dev to Master.

In VSCode Git view: Click "Publish Branch" to push dev to GitHub/Anvil.

Go to GitHub.com (your repo page), click "Compare & pull request" button—it shows changes.

Review the differences, click "Create pull request," then "Merge pull request"—done! Master updates.

Step 5: Repeat and Watch
Delete the dev branch after merge (right-click in VSCode).

Measure time: From AI code to test should be under 1 minute—adjust if slow.

Next feature: New dev branch, repeat steps 2-4.

This keeps errors tiny and caught fast, per the video rules. Which step to explain more?