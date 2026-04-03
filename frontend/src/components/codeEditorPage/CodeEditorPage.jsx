import styles from "../../css/CodeEditor.module.css"
import {ProjectStructure} from "./ProjectStructure.jsx";
import {createContext, useMemo, useState} from "react";
import {EditorField} from "./EditorField.jsx";
import {CommitContextMenu} from "./CommitContextMenu.jsx";
import {RollbackContextMenu} from "./RollbackContextMenu.jsx";

export const FileContext = createContext(null)

export const CodeEditorPage = () => {

  const [currentFile, setCurrentFile] = useState(null)
  const [globalContextMenu, setGlobalContextMenu] = useState(null)

  const contextCurrentFile = useMemo(() => ({
    currentFile: currentFile,
    setCurrentFile: setCurrentFile,
  }), [currentFile]);

  return (
      <FileContext.Provider value={contextCurrentFile}>
        <div className={styles.content}>
          <ProjectStructure />
          <EditorField globalContextMenu={globalContextMenu} setGlobalContextMenu={setGlobalContextMenu}/>
          {globalContextMenu === "commit" && <CommitContextMenu globalContextMenu={globalContextMenu}
                                                                setGlobalContextMenu={setGlobalContextMenu}/>}
          {globalContextMenu === "rollback" && <RollbackContextMenu setGlobalContextMenu={setGlobalContextMenu}/>}
        </div>
      </FileContext.Provider>

  )
}