import styles from "../../css/Function.module.css";
import {getStringDate} from "../../utils/formats.js";

export const FunctionDescription = ({description}) => {

  return (
      <div className={styles.functionDescription}>
            <div className={styles.parameter}>
              <span className={styles.head}>ID: </span>{description.id}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Дата создания: </span>{getStringDate(description.createdAt)}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Сервис: </span>{description.service}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Окружение: </span>{description.environment}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Путь к обработчику: </span>{description.handlerPath}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Обработчик: </span>{description.handler}
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Размер памяти: </span>{description.memorySize} МБ
            </div>
            <div className={styles.parameter}>
              <span className={styles.head}>Таймаут: </span>{description.timeout} с
            </div>
        </div>
  )
}