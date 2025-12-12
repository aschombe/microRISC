#import "rivet-config.typ": schema, config, rivet-config

#set page(
  paper: "a4",
  numbering: "<1>",
)

#set text(
  font: "Inconsolata",
  size: 12pt,
)

#set document(
  title: "microRISC",
  author: "Andrew Schomber",
)

#align(horizon)[
  #align(center)[
    #text(size: 32pt)[
      #context(document.title)
    ]
    #linebreak()
    #text(size: 16pt)[
      #text(size: 16pt)[
        #context(document.author).at(0)
      ]
    ]
    #linebreak()
    #datetime.today().display("[month repr:long] [day], [year]")
  ]
]

#pagebreak()

#show outline.entry.where(level: 1): it => {
  v(14pt, weak: true)
  strong(it)
}

#show outline.entry: it => link(
  it.element.location(),
  it.indented(
    [
      #it.prefix()
      → 
    ],
    it.inner(),
  ),
)

#outline(
  title: [Table of Contents],
  indent: 1.2em,
)

#pagebreak()

#include "sections/section1.typ"
#pagebreak()
#include "sections/section2.typ"
