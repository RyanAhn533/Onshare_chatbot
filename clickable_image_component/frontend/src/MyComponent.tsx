import React, { useState } from "react"
import { Streamlit, withStreamlitConnection } from "streamlit-component-lib"

const MyComponent = (props: any) => {
  const { images } = props.args
  const [selected, setSelected] = useState<string[]>([])

  const toggle = (name: string) => {
    const updated = selected.includes(name)
      ? selected.filter(n => n !== name)
      : [...selected, name]
    setSelected(updated)
    Streamlit.setComponentValue(updated)
  }

  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: "16px" }}>
      {images.map((src: string, idx: number) => (
        <div key={idx} onClick={() => toggle(src)}
             style={{
               cursor: "pointer",
               border: selected.includes(src) ? "4px solid orange" : "2px solid #ccc",
               borderRadius: "12px",
               padding: "4px"
             }}>
          <img src={src} style={{ width: "150px", height: "auto", borderRadius: "8px" }} />
        </div>
      ))}
    </div>
  )
}

export default withStreamlitConnection(MyComponent)
