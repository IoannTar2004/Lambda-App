import styles from "../../css/CodeEditor.module.css"
import {ProjectStructure} from "./ProjectStructure.jsx";
import {createContext, useMemo, useState} from "react";
import Editor from "@monaco-editor/react";
import {EditorField} from "./EditorField.jsx";

export const FileContext = createContext(null)

export const CodeEditorPage = () => {

  const [currentContent, setCurrentContent] = useState({name: "", upload: null})

  const contextCurrentContent = useMemo(() => ({
    currentContent,
    setCurrentContent
  }), [currentContent]);

  return (
      <FileContext.Provider value={contextCurrentContent}>
        <div className={styles.content}>
          <ProjectStructure />
          <EditorField />
        </div>
      </FileContext.Provider>

  )
}