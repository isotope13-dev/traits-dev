import Events from 'event-pubsub';
import {createParser} from '../entities/EventParser.js';
import net from 'node:net';
import tls from 'node:tls';
class Server extends Events { start(){this.a=net.createServer(()=>{});this.b=tls.createServer({},()=>{});}}
