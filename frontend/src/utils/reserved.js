const reservedFiles = [
    ".dir" // Файл, который есть в каждой директории S3. Служит для ее существования в случае отсутствия пользовательских файлов.
]

export const isReservedFile = (name) => {
    return reservedFiles.includes(name)
}

// Некоторые данные, такие как бакет S3 содержат дополнительную информацию в названии. Ее не нужно выводить пользователю.
const metaNames = {
    "bucket": (e) => e.split("-").slice(1).join("-")
}

export const deleteMetaFromName = (key, name) => {
    const fn = metaNames[key];
    return fn ? fn(name) : name;
}