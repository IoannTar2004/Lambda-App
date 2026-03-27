import styles from "../../css/CodeEditor.module.css"
import EditorField from "./EditorField.jsx";
import {ProjectStructure} from "./ProjectStructure.jsx";

export const CodeEditorPage = () => {

  return (
      <div className={styles.content}>
          <ProjectStructure />
      </div>
      // <EditorField />
  )
}