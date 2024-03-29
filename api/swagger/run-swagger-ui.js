const express = require('express')
const pathToSwaggerUi = require('swagger-ui-dist').absolutePath()

const app = express()

app.use(express.static(pathToSwaggerUi))
app.use(express.static(`${__dirname}`))

app.listen(3000)
