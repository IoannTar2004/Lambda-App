import {FaJava, FaPython} from "react-icons/fa";
import {IoLogoJavascript} from "react-icons/io";

export const languageExtensionIcons = {
    "py": <FaPython className={"icon"} />,
    "java": <FaJava className={"icon"} />,
    "js": <IoLogoJavascript className={"icon"} />
}

export const getLanguageIconByExtension = (filename) => {
    const extension = filename.split(".").pop()
    return languageExtensionIcons[extension]
}