if (process.env.MODE !== 'production') {
    require('dotenv').config()
}

export const serviceName = process.env.SERVICE_NAME || ''
export const port = Number(process.env.PORT) || 4000
export const host = process.env.HOST || ''
export const azureEndpointUri = process.env.AZURE_ENDPOINT_URI || ''
export const azurePrimaryKey = process.env.AZURE_PRIMARY_KEY || ''
export const mode = process.env.MODE || ''