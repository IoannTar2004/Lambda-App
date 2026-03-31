export const isReservedName = (name) => {
    return reservedFiles.includes(name)
}

const reservedFiles = [
    ".dir" // файл, который есть в каждой директории S3. Служит для ее существования в случае отсутствия пользовательских файлов
]