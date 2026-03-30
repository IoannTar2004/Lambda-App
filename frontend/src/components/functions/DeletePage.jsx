import styles from "../../css/Function.module.css"

export const DeletePage = () => {
  return (
    <div className={styles.modalContent}>
      <div className={styles.formWindow + " " + styles.center}>
        <div style={{fontSize: "20px"}}>Вы уверены, что хотите удалить функцию?</div>
        <button id={styles.deleteFunctionButton}>Удалить</button>
      </div>
    </div>
  )
}