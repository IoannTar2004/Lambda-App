import styles from "../../css/CodeEditor.module.css"
import {ProjectStructure} from "./ProjectStructure.jsx";
import {createContext, useMemo, useState} from "react";
import Editor from "@monaco-editor/react";
import {EditorField} from "./EditorField.jsx";

export const FileContext = createContext(null)

export const CodeEditorPage = () => {

  const [currentFile, setCurrentFile] = useState(null)

  const contextCurrentFile = useMemo(() => ({
    currentFile: currentFile,
    setCurrentFile: setCurrentFile
  }), [currentFile]);

  return (
      <FileContext.Provider value={contextCurrentFile}>
        <div className={styles.content}>
          <ProjectStructure />
          <EditorField />
        </div>
      </FileContext.Provider>

  )
}