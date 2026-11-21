# Security Guardian for an AI Agent

## How to run it


1. Create the virtual environment 
   ```bash
   python -m venv .venv
   ```

2. Activate it (every time you open a new terminal):

   ```bash
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

   # Windows (cmd)
   .venv\Scripts\activate.bat

   # Windows (Git Bash)
   source .venv/Scripts/activate

   # macOS / Linux
   source .venv/bin/activate
   ```


3. Install the dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run it:

   ```bash
   python -m guardian corpus/semilla/sesion_semilla.txt
   ```

> If PowerShell says running scripts is disabled, run this once and try again:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

## Structure

```
guardian/
├── __main__.py        entry point                      
├── models.py          shared data types               
├── loader.py          reads the file and the mode      
├── dispatcher.py      runs the analysis of each line  
├── report.py          prints the results               
├── call/              First analysis of the action
├── sql/               SQL lexer and parser               [P2]
├── url/               URL lexer, parser and R5–R7       [P3]
├── pda/               pushdown automaton               [P4]
└── semantics/         R1–R4, R8, verdict               [P4]
corpus/semilla/        sample input files
```

## Architecture

```
file.txt
   │
   ▼
loader ──► mode and list of lines
   │
   ▼  
call ──► origin, tool, argument
   │
   ▼
dispatcher ──┬─► consultar_bd → sql  (lexer → pda → parser)
             └─► abrir_enlace → url  (lexer → parser)
   │
   ▼  (only if there were no lexical or syntax errors)
semantics ──► rules R1–R8
   │
   ▼
verdict ──► ALLOW | CONFIRM | BLOCK | ERROR
   │
   ▼
report ──► console
```
