import styles from "../../css/CodeEditor.module.css";
import {FaAngleDown} from "react-icons/fa";
import {AiFillFileAdd} from "react-icons/ai";
import {RiFolderAddFill} from "react-icons/ri";

export const ProjectStructure = () => {
  return (
      <div className={styles.projectStructureBox}>
        <div className={styles.directory}>
          <div className={styles.projectName}>
            <span><FaAngleDown className={"icon"} size={"22px"}/></span>
            <span>my_project</span>
          </div>

          <div className={styles.toolsBox}>
            <AiFillFileAdd className={"icon " + styles.tool} />
            <RiFolderAddFill className={"icon " + styles.tool} />
          </div>
        </div>

      </div>
  )
}