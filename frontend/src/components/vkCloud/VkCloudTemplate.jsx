import styles from "../../css/VkCloudTemplate.module.css"
import vkCloudMenu from "../../assets/vk-cloud-menu.png"
import vkCloudHeader from "../../assets/vk-cloud-header.jpeg"
import {Outlet} from "react-router";

export const VkCloudTemplate = () => {
  return (
      <div className={styles.content}>
        <img src={vkCloudMenu} alt="menu" />
        <div className={"app"}>
          <img className={styles.vkСloudHeaderStub} src={vkCloudHeader} alt="header" />
          <Outlet />
        </div>
      </div>
  )
}