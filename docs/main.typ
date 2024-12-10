#import "@preview/curryst:0.3.0": rule, proof-tree

#set page(
  paper: "a4",
  numbering: "<1>",
)

#set text(
  font: "Inconsolata",
  size: 12pt,
)

#set document(
  title: "CS516: Compiler Design & Implementation Notes",
  author: "Andrew Schomber",
)

#align(horizon)[
  #align(center)[
    #text(size: 32pt)[
      #context(document.title)
    ]
    #linebreak()
    #text(size: 16pt)[
      // #context(document.author) isn't working for some reason, it inserts ("Andrew Schomber",) onto the page
      Andrew Schomber
    ]
    #linebreak()
    #datetime.today().display("[month repr:long] [day], [year]")
  ]
]

#pagebreak()

#show outline.entry.where(
  level: 1
): it => {
  v(14pt, weak: true)
  strong(it)
}

#outline(
  title: "Table of Contents",
  indent: n => [→ ] * n,
)

#pagebreak()

#include "sections/section1.typ"
#pagebreak()
#include "sections/section2.typ"
