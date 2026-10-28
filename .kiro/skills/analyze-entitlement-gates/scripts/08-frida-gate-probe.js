// Gate probe — observe first, force on the second run.
// RUNTIME: only use within a scope that permits instrumentation (assets/scope.json),
// after confirming the action with the operator.
//   frida -U -f <bundleId> -l 08-frida-gate-probe.js    (spawn, iOS/Android)
//   frida -p <pid>        -l 08-frida-gate-probe.js    (attach, desktop)
// Edit CONFIG. forceReturn: null = observe only.
const CONFIG = {
  objc:    [{ cls: "EntitlementManager", method: "- isPro" }], // iOS/macOS
  symbols: ["_is_premium_enabled"],                            // exported
  offsets: [/* { module: "App", offset: "0x1007d4" } */],       // native
  forceReturn: null,       // true | 1 | "0x1" once the baseline is captured
};

function report(where, args, retval) {
  send({ where, args: args.map(a => a?.toString?.() ?? String(a)), retval: String(retval) });
}

setTimeout(() => {
  if (typeof ObjC !== "undefined") {
    for (const { cls, method } of CONFIG.objc) {
      try {
        const owner = ObjC.classes[cls];
        if (!owner) { send({ where: cls, note: "class not found" }); continue; }
        const impl = owner[method.split(":")[0]] && owner[method.split(":")[0]].implementation;
        if (!impl) { send({ where: `${cls} ${method}`, note: "selector not found" }); continue; }
        Interceptor.attach(impl, {
          onEnter(a) { this.a = [a[2], a[3], a[4]]; },
          onLeave(r) {
            report(`${cls} ${method}`, this.a, r);
            if (CONFIG.forceReturn !== null) r.replace(CONFIG.forceReturn);
          },
        });
        send({ where: `${cls} ${method}`, note: "hooked" });
      } catch (e) { send({ where: cls, error: String(e) }); }
    }
  }
  for (const name of CONFIG.symbols) {
    try {
      const p = Module.getGlobalExportByName
        ? Module.getGlobalExportByName(name)
        : Module.findExportByName(null, name);
      if (!p) { send({ where: name, note: "export not found" }); continue; }
      Interceptor.attach(p, {
        onEnter(a) { this.a = [a[0], a[1], a[2]]; },
        onLeave(r) {
          report(name, this.a, r);
          if (CONFIG.forceReturn !== null) r.replace(CONFIG.forceReturn);
        },
      });
      send({ where: name, note: "hooked" });
    } catch (e) { send({ where: name, error: String(e) }); }
  }
  for (const { module, offset } of CONFIG.offsets) {
    try {
      const base = Process.getModuleByName(module).base;
      const addr = base.add(ptr(offset));
      Interceptor.attach(addr, {
        onEnter(a) { this.a = [a[0], a[1], a[2]]; },
        onLeave(r) {
          report(`${module}+${offset}`, this.a, r);
          if (CONFIG.forceReturn !== null) r.replace(CONFIG.forceReturn);
        },
      });
      send({ where: `${module}+${offset}`, note: "hooked" });
    } catch (e) { send({ where: `${module}+${offset}`, error: String(e) }); }
  }
}, 0);
