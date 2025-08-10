dot = """
digraph ResearcherAgent {
    rankdir=LR;
    splines=true;
    bgcolor="transparent";
    fontsize=14;
    fontname="Segoe UI, Tahoma, Geneva, Verdana, sans-serif";

    node [
        shape=box,
        style="filled,rounded,shadow",
        fontname="Segoe UI",
        fontsize=12,
        color="#5B9BD5",
        fillcolor="#D9E8FB",
        margin=0.3,
        width=2,
        height=1.0
    ];

    __start__ [
        label="Start",
        shape=circle,
        style="filled,shadow",
        fillcolor="#5B9BD5",
        color="#2F5597",
        width=0.6,
        fixedsize=true
    ];
    
    Researcher [
        label="Researcher Agent",
        fillcolor="#8AB6D6",
        color="#4A90E2"
    ];

    tool_condition [
        label="Tool Condition",
        shape=diamond,
        style="filled,shadow",
        fillcolor="#F9D57E",
        color="#D49A00",
        width=1.6,
        height=1.4
    ];

    Writer [
        label="Writer",
        fillcolor="#A0D468",
        color="#6DA600"
    ];

    __end__ [
        label="End",
        shape=doublecircle,
        style="filled,shadow",
        fillcolor="#5B9BD5",
        color="#2F5597",
        width=0.7,
        fixedsize=true
    ];

    edge [
        fontname="Segoe UI",
        fontsize=11,
        color="#555555",
        penwidth=2,
        arrowsize=1.2,
        arrowhead="vee",
        smoothType="cubic"
    ];

    __start__ -> Researcher;
    Researcher -> tool_condition;

    tool_condition -> __end__ [label="tools NOT used", color="#E94B3C", fontcolor="#E94B3C"];
    tool_condition -> Writer [label="tools used", color="#4CAF50", fontcolor="#4CAF50"];

    Writer -> __end__;
}
"""
