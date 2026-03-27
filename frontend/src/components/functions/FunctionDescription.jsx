import styles from "../../css/Function.module.css";

export const FunctionDescription = ({functionData}) => {

  return (
      <div className={styles.functionDescription}>
            <div className={styles.parameter}>
              <span className={styles.head}>ID: </span>{functionData.id}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Дата создания: </span>26.03.2026 в 15:00
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Последний вызов: </span>26.03.2026 в 15:00
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Сервис: </span>{functionData.service}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Окружение: </span>{"Python 3.12"}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Путь к обработчику: </span>{"a".repeat(256)}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Обработчик: </span>{functionData.handler}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Размер памяти: </span>{1024} МБ
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Таймаут: </span>{300} с
            </div>
        </div>
  )
}