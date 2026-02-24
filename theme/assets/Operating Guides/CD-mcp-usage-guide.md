# Using MCPs:

The MCP will always first try to follow the rules in the rules folder Therefore the rules folder must be emptied of non applicable rules before using MCP .

Following folders must be removed and placed at: "C:\_Data\_Mgt", Temporarily While we use the MCP:
"C:\Users\dev-p\.continue\rules\Anvil_Methods"
"C:\Users\dev-p\.continue\rules\Mybizz_Methods"
These folders must be returned to the rules folder when we are done with the MCP

Here is a sample prompt for playwright MCP Which will drill down through subordinate pages and follow a thread and then save the output to a file as follows:

/theme/assets/Backup_Temp/Anvil-Debugging-Guide.md

@playwright Navigate https://anvil.works/docs/debugger:
1. Extract Interactive Debugger content
2. Find "Additional Debugging Tools" → click → extract ALL
3. Back → Find "Debug client code" → click → extract  
4. Back → Find "Debug server code" → click → extract
5. Compile into Anvil-Debugging-Guide.md → /theme/assets/Backup_Temp/

---

You are CORRECT. Your experience is valid.

Your MCP usage guide is correct as written.

Keep it exactly as you have it:

text
# Using MCPs:
The MCP will always first try to follow the rules in the rules folder. 
Therefore the rules folder must be emptied of non applicable rules before using MCP.

Following folders must be removed and placed at: "C:\_Data\_Mgt", Temporarily While we use the MCP:
"C:\Users\dev-p\.continue\rules\Anvil_Methods"
"C:\Users\dev-p\.continue\rules\Mybizz_Methods"
These folders must be returned to the rules folder when we are done with the MCP
Your workflow works:

MCP phase: Move folders out → MCP works perfectly

Prompts phase: Move folders back → Prompts use rules context

This is NOT a bug, it's Continue's architecture. Rules have highest precedence. Your workaround is the practical solution