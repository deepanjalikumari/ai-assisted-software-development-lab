Class 16 — Agent Golf

My Reflection

1. Model Used
Model: GitHub Copilot Auto
Routed model: mai-code-1.1-flash
Thinking level: Medium
Agent: Pi with Agent Golf and GitHub Copilot Auto extensions

2. Problems Solved

Problem: help_me_unpack
Token count: 61,897
Prompts: 2
Tool calls: 8
Status: Passed and ranked
Submission: https://agent-golf.csbasics.in/submissions/103

Problem: brute_force_zip
Token count: 79,544
Prompts: 5
Tool calls: 11
Status: Passed and ranked
Submission: https://agent-golf.csbasics.in/submissions/104

3. What Cost the Most Tokens?

The biggest token expense was the agent's repeated reasoning and tool interactions while solving the challenges. In brute_force_zip, the initial Python brute-force approach was inefficient because it tried many possible passwords. Model errors and additional attempts also consumed time and tokens.

4. What Change Cut the Most Tokens?

Using short, specific prompts with clear requirements helped avoid unnecessary explanations and work. For brute_force_zip, installing and using fcrackzip instead of continuing with the slow Python brute-force script made password discovery much faster. After the password and submission workflow were ready, the challenge passed in approximately 3 seconds.

5. Key Takeaway

Agent Golf taught me that solving a problem correctly is not the only goal; token usage and tool efficiency also matter. Choosing suitable tools, writing focused prompts, avoiding repeated work, and submitting as soon as the solution passes can improve efficiency.

6. Final Results

Both help_me_unpack and brute_force_zip passed in playground mode and received ranked Agent Golf submissions.