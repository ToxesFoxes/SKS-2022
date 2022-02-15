const Generator = {
  header() {
    return `!\nversion 12.1\nno service timestamps log datetime msec\nno service timestamps debug datetime msec\nno service password-encryption\n!\nhostname Switch\n!\n!\n!\n!\n!\n!\nspanning-tree mode pvst\nspanning-tree extend system-id\n`
  },
  interface(name, vlan, type) {
    if (vlan) return `!\ninterface FastEthernet0/${name}\n switchport ${type || 'access'} vlan ${vlan}\n`
    else return '!\ninterface FastEthernet${name}\n';
  },
  footerD() {
    return `!\ninterface FastEthernet0/22\n!\ninterface FastEthernet0/23\n!\ninterface FastEthernet0/24\n switchport trunk allowed vlan 2-1001\n switchport mode trunk\n!\ninterface Vlan1\n no ip address\n shutdown\n!\n!\n!\n!\nline con 0\n!\nline vty 0 4\n login\nline vty 5 15\n login\n!\n!\n!\n!\nend\n\n`
  },
  footerC() {
    return `!\ninterface FastEthernet0/22\n switchport mode trunk\n!\ninterface FastEthernet0/23\n!\ninterface FastEthernet0/24\n switchport trunk allowed vlan 2-1001\n switchport mode trunk\n!\ninterface Vlan1\n no ip address\n shutdown\n!\n!\n!\n!\nline con 0\n!\nline vty 0 4\n login\nline vty 5 15\n login\n!\n!\n!\n!\nend\n\n`
  }
}
class Switch {
  type = 0
  vlan = 10
  result = ''
  constructor(vlan, type) {
    if (vlan)
      this.vlan = vlan
    if (type)
      this.type = type
  }
  build() {
    this.result += Generator.header()
    for (let i = 1; i <= 18; i++) {
      this.result += Generator.interface(i, this.vlan, 'access')
    }
    for (let i = 19; i <= 21; i++) {
      this.result += Generator.interface(i, this.vlan, 'voice')
    }
    if (this.type == 1)
      this.result += Generator.footerC()
    else 
      this.result += Generator.footerD()
    return this.result
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
rl.question("Input (vlanId type): ", function (str) {
  // console.log(`You are ${age} years old`)
  let { n1, n2 } = { n1: Number(str.split(' ')[0]), n2: Number(str.split(' ')[1])}
  let res = new Switch(n1, n2)
  res.build()
  console.log(res.getBuildResult())
  rl.close()
})

rl.on("close", function () {
  process.exit(0)
})