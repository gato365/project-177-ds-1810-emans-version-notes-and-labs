-- {{< vspace >}}          -> 2rem of vertical space (HTML) / 2em (PDF)
-- {{< vspace 3rem >}}     -> any CSS length
-- Use it between an H1 section and the H2 that follows, or anywhere the page
-- needs breathing room. Renders as an empty block, never as text.
return {
  ["vspace"] = function(args, kwargs, meta)
    local size = (args[1] and pandoc.utils.stringify(args[1])) or "2rem"
    if quarto.doc.is_format("html") then
      return pandoc.RawBlock("html",
        '<div class="vspace" style="height:' .. size .. '" aria-hidden="true"></div>')
    elseif quarto.doc.is_format("pdf") then
      return pandoc.RawBlock("latex", "\\vspace{" .. size:gsub("rem", "em") .. "}")
    else
      return pandoc.Para({})
    end
  end
}
