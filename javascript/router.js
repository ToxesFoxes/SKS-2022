var DhcpPool = {
	id(id) {
		return `ip dhcp pool p${id}\n`
	},
	network(id) {
		return ` network 192.168.${id}.0 255.255.255.0\n`
	},
	defRouter(id) {
		return ` default-router 192.168.${id}.254\n`
	},
	option(id) {
		return ` option 150 ip 192.168.${id}.254\n`
	},
	getPool(id) {
		return this.id(id) + this.network(id) + this.defRouter(id) + this.option(id)
	},
	genMultiple(from, to) {
		let result = '!\n'
		for (let i = from; i <= to; i++)
			result += this.getPool(i)

		return result
	},
	excludeMultiple(from, to) {
		var result = '!\n'
		for (let i = from; i <= to; i++)
			result += this.exclude(i)

		return result
	},
	exclude(i) {
		return `ip dhcp excluded-address 192.168.${i}.254\n`
	}
}
const DialPeer = {
	add(n1, n2, n3) {
		return `!\ndial-peer voice ${n1}00 voip\n destination-pattern ${n2}..\n session target ipv4:${n3 >= 10 ? Math.floor(24 / 10) + '' + (n3 % 10) : '1' + n3}.0.0.2\n`
	},
	genDialPeer(count, excludedId) {
		let result = ''
		for (let i = 1; i <= count; i++) {
			if (i !== excludedId) {
				result += this.add(i, i, i - 1)
			}
		}
		return result
	},
}
const Telephony = {
	service(max, ip) {
		return `!\ntelephony-service\n max-ephones ${max}\n max-dn ${max}\n ip source-address ${ip}.0.0.2 port 2000\n auto assign 1 to ${max}\n`
	},
	ephone(num, mac) {
		return `!\nephone ${num}\n device-security-mode none\n mac-address ${mac}\n type 7960\n button 1:${num}\n`
	},
	genEphone(count, macList) {
		let result = ''
		for (let i = 1; i <= count; i++)
			result += this.ephone(i, macList[i - 1])
		return result
	},
	ephoneDn(i, num) {
		return `!\nephone-dn ${i}\n number ${num}\n`
	},
	genEphoneDn(prefix, count) {
		let result = ''
		for (let i = 1; i <= count; i++)
			result += this.ephoneDn(i, prefix + i)

		return result
	}
}
const RouterConstructor = {
	genHeader(name) {
		return `!\nversion 15.1\nno service timestamps log datetime msec\nno service timestamps debug datetime msec\nno service password-encryption\n!\nhostname ${name}\n!\n!\n!\n`
	},
	addAfterPool(udiPid) {
		return `!\n!\n!\nno ip cef\nno ipv6 cef\n!\n!\n!\n!\nlicense udi pid CISCO2811/K9 sn ${udiPid || 'undefined'}\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\n!\nspanning-tree mode pvst\n!\n!\n!\n!\n!\n`
	},
	genFooter() {
		return `!\nline con 0\n!\nline aux 0\n!\nline vty 0 4\n login\n!\n!\n!\nend\n\n`
	},
	eigrp(globalNetId, from, to) {
		let result = `!\nrouter eigrp 50\n network ${globalNetId}.0.0.0\n`
		for (let i = from; i <= to; i++)
			result += ` network 192.168.${i}.0\n`
		return result
	},
	addAfterEigrp() {
		return `!\n!\nrouter rip\n!\nip classless\n!\nip flow-export version 9\n!\n!\n!\n!\n!\n!\n!\n`
	}
}
const interface = {
	genDefault(name, sh) {
		let result = '!\n'
		result += `interface FastEthernet${name}\n`
		result += ` no ip address\n`
		result += ` duplex auto\n`
		result += ` speed auto\n`
		if (sh)
			result += ' shutdown\n'
		return result
	},
	genSubInt(name, subNetId) {
		let result = '!\n'
		result += `interface FastEthernet${name}.${subNetId}\n`
		result += ` encapsulation dot1Q ${subNetId}\n`
		result += ` ip address 192.168.${subNetId}.254 255.255.255.0\n`
		return result
	},
	genSerial(name, subNetId) {
		let result = '!\n'
		result += `interface Serial${name}\n`
		result += ` ip address ${subNetId}.0.0.2 255.0.0.0\n`
		return result
	},
	getVlan() {
		return '!\ninterface Vlan1\n no ip address\n shutdown\n'
	}
}
// const res = Routerd.build('Router ы', 1, 10, 1, 15)
// console.log(res)

class Router {
	name = 'Router'
	subNetId = 0
	dialPeerId = 0
	buildingCount = 15
	globalNetId = 10
	result = ''
	udiPid = 'undefined'
	macList = []
	constructor(subNetId, dialPeerId, globalNetId, udiPid, macList) {
		if (subNetId)
			this.subNetId = subNetId
		if (dialPeerId)
			this.dialPeerId = dialPeerId
		if (udiPid)
			this.udiPid = udiPid
		if (macList)
			this.macList = macList
		if (globalNetId)
			this.globalNetId = globalNetId
	}
	set name(name) {
		this.name = name
	}
	set subNetId(subNetId) {
		this.subNetId = subNetId
	}
	set dialPeerId(dialPeerId) {
		this.dialPeerId = dialPeerId
	}
	set buildingCount(buildingCount) {
		this.buildingCount = buildingCount
	}
	build() {
		this.result += RouterConstructor.genHeader(this.name)
		this.result += DhcpPool.excludeMultiple(this.subNetId, this.subNetId + 2)
		this.result += DhcpPool.genMultiple(this.subNetId, this.subNetId + 2)
		this.result += RouterConstructor.addAfterPool(this.udiPid)
		this.result += Interface.genDefault('0/0', true)
		this.result += Interface.genDefault('0/1', false)
		this.result += Interface.genSubInt(`0/1`, this.subNetId)
		this.result += Interface.genSubInt(`0/1`, this.subNetId + 1)
		this.result += Interface.genSubInt(`0/1`, this.subNetId + 2)
		this.result += Interface.genSerial('0/1/0', this.globalNetId)
		this.result += Interface.getVlan()
		this.result += RouterConstructor.eigrp(this.globalNetId, this.subNetId, this.subNetId + 2)
		this.result += RouterConstructor.addAfterEigrp()
		this.result += DialPeer.genDialPeer(this.buildingCount, this.dialPeerId, this.subNetId)
		this.result += Telephony.service(9, this.globalNetId)
		this.result += Telephony.genEphoneDn(this.dialPeerId * 100, 9)
		this.result += Telephony.genEphone(9, ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
		this.result += RouterConstructor.genFooter()
	}
	getBuildResult() {
		return this.result
	}
}

const readline = require("readline")
const rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout
})
// rl.close()
rl.question("Input (SubNetId DialPeerId GlobalNetId): ", function (str) {
	// console.log(`You are ${age} years old`)
	let { n1, n2, n3 } = { n1: Number(str.split(' ')[0]), n2: Number(str.split(' ')[1]), n3: Number(str.split(' ')[2]) }
	let res = new Router(n1, n2, n3)
	res.build()
	console.log(res.getBuildResult())
	rl.close()
})

rl.on("close", function () {
	process.exit(0)
})