// import Server from './server/index'
import { mode } from './config'

console.log("cum");

const origin: string | string[] = (mode === 'development')
    ? ["http://127.0.0.1:3000", "http://localhost:3000", "http://192.168.20.14:3000"]
    : "https://organisemymeals.com"

const server = new Server(origin)

server.start()
