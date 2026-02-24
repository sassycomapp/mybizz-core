Anvil Debugging Guide

## Introduction

Debugging is an essential part of building reliable applications, and the Anvil Editor makes it seamless with a suite of powerful tools.

The **Interactive Debugger** in Anvil lets you pause and inspect your code in real time, whether on the **client** or **server side**, helping you diagnose and resolve issues efficiently.

![The Anvil Interactive Debugger demo.](https://anvil-website-static.s3.eu-west-2.amazonaws.com/docs/debugging/using-the-debugger-repl.gif)

The Anvil Editor also provides additional tools to give you complete visibility into your app’s execution:

1. **Server Console:** A Python REPL allowing you to execute server-side code, test functions, and interact with custom Python packages.
2. **App Console:** A real-time REPL for interacting with your app’s UI components, inspecting properties, and triggering client and server side methods.

Together, these tools give you full visibility into your app’s execution, making it easier to debug and refine your code.

## Interactive Debugger

The Anvil Editor has a built-in **Interactive Debugger** that allows you to pause execution and inspect your code in real time, both on the **client and server side**. It provides tools to help you quickly diagnose and fix issues in your app.

### Key Features

1. **Add and Remove Breakpoints:** Pause code execution at specific areas in your code both on client and server side. You can also pause on server code called from the client.
2. **Explore the Call Stack:** Explore the call stack across client-server boundaries and inspect variables and values at runtime.
3. **Step Through Code:** Easily navigate through code execution across both client-side and server-side code, with the debugger tools.
4. **Interact with Objects in the Debugger REPL:** Directly interact with your application’s state while debugging.
5. **Safe Debugging Environment:** Breakpoints only activate in your Development Environment and are ignored in published versions of your app.
6. **Debug Background Tasks and HTTP Endpoints:** The debugger stops at all breakpoints in your Development Environment, including in Background Tasks and HTTP Endpoints.

All users can use the debugger in **client code**. You will need to be on the Business Plan or above to stop at breakpoints in **Server Code**.

### How it Works

When you add a breakpoint to an executable line of code in the anvil editor, and run your code, your app will work as normal until execution reaches the breakpoint (the breakpoint is hit). Here is what happens then:

1. **Code execution is paused** just before the line of code is executed.
2. The **line of code** where execution is paused (usually at a breakpoint) is **highlighted**, as well as its call sites. This highlight color changes depending on whether the editor is in light or dark mode
3. The **Debugger Window** opens, showing all local and global variables, within the scope of the breakpoint or selected call stack frame, along with the Debugger console, where you can interact with these variables.

### Adding and Removing Breakpoints

Breakpoints are marked by a red circle icon in the gutter of the Anvil editor. They allow you to pause execution at specific points in your code. You can add or remove breakpoints in both client and server code at any time:

* Before execution begins.
* While your code is running.
* When execution is paused.

**Tip:** If execution is paused and you want to quickly skip to the end of a block of code, place a new breakpoint at the end of that block and click **Resume**. Execution will continue until it reaches the new breakpoint.

#### Adding Breakpoints

You can add breakpoints to any executable line of code:

1. Click the gutter next to the line of code you want to debug.
2. A red circle icon will appear, marking your breakpoint.

#### Removing Breakpoints

The breakpoint behaves like a toggle, clicking on a breakpoint will remove it.

![Add and remove breakpoints](img/interactive-debugger/add-remove-breakpoints.gif)

**Note:** Adding a breakpoint to an unexecutable line of code like a function definition will not pause execution. Breakpoints should be added to executable lines of code, such as those inside the function body or anywhere the function is called.

### The Debugger Window

![Labeled components of the Debugger Window.](https://anvil-website-static.s3.eu-west-2.amazonaws.com/docs/debugging/debugger.png)

1. **Call Stack:** Displays the current line of code whose breakpoint was hit and its call stack.
2. **Debugger Toolbar:** Provides common debugging actions like stepping through code.
3. **Object Inspector:** Shows all variables in your code, including local and global scopes.
4. **Debugger REPL:** A Python REPL where you can interact with all the local and global variables within the scope of the selected call stack frame as well as all the modules and packages in your app.

#### The Call Stack

The call stack shows the sequence of function calls that led to a breakpoint. The call stack starts from the paused execution point and traces back through the call history.

Clicking on a call stack frame **opens that line of code** in your project and **updates the variables** in the Object inspector to reflect the objects within the context of that line of code.

![Clicking on a call stack frame](https://anvil-website-static.s3.eu-west-2.amazonaws.com/docs/debugging/call-stack-frame.gif)

The call stack is grouped into two sections: **Browser** for client-side calls and **Server** for server-side calls.

#### The Debugger Toolbar

- ![Resume](img/interactive-debugger/resume.png) **Resume:** Continue executing indefinitely, or until the next breakpoint.
- ![Restart](img/interactive-debugger/restart.png) **Restart:** Stop the current process and restart your application.
- ![Stop](img/interactive-debugger/stop.png) **Stop:** Terminate the current process.
- ![Step Over](img/interactive-debugger/step-over.png) **Step Over:** Execute the current line and pause on the next line.
- ![Step Into](img/interactive-debugger/step-in.png) **Step Into:** If a function call, go into it; otherwise step over.
- ![Step Out](img/interactive-debugger/step-out.png) **Step Out:** Execute to the end of the current function.

#### Object Inspector

Displays all objects in the current scope: **Local Variables** and **Global variables**.

Expand/collapse by clicking arrows.

![Expand and collapse variables](https://anvil-website-static.s3.eu-west-2.amazonaws.com/docs/debugging/expand-and-collapse-objects.gif)

#### The Debugger REPL

Interact with application state.

- Interact with objects in scope and modules/packages.
- Create variables (appear in inspector).
- Use `global` for global vars.

Server-side: orange line; Client-side: blue line.

![Updating a Variable’s Value in the Debugger REPL](https://anvil-website-static.s3.eu-west-2.amazonaws.com/docs/debugging/using-the-debugger-repl.gif)

Console history appears in Running App Console after session.

### Debugging Background Tasks and HTTP Endpoints

Breakpoints work in Development Environment for Background Tasks and HTTP Endpoints.

## Additional Debugging Tools

### Server Console

A Python REPL with all custom packages.

#### Accessing Server Functions

```python
import server_module_name
server_module_name.function(...)
```

Example:
```python
import ServerModule1 
ServerModule1.add_person_to_table(name=\"Love\", workplace=\"Anvil\")
```

![People table](img/additional-debugging-tools/people-table-image.png)

#### Interacting with Custom Packages

```python
import numpy
a = numpy.array([2, 4, 6])
print(a)
```

![NumPy array output](img/additional-debugging-tools/numpy-output.png)

### Running App Console (Debug Client Code)

Interact with running app.

#### Accessing Components

```python
form = get_open_form()
```

#### Calling Methods

```python
form.refresh_data_bindings()
```

Call server functions with `anvil.server.call(...)`

#### Inspect and Update UI Properties

```python
form.refer_drop_down.items
form.refer_drop_down.items = ['No', 'Yes']
```

![Drop-down items](img/additional-debugging-tools/refer-dropdown-items.png)
![Updated drop-down items](img/additional-debugging-tools/updated-dropdown-items.png)

## Notes

- Business Plan+ required for server breakpoints in Interactive Debugger.
- Breakpoints only in Development Environment.
- Server Console for server-side testing.
- Running App Console for client-side interaction while app runs.

Compiled from Anvil Docs: https://anvil.works/docs/debugger and subpages on 2024.