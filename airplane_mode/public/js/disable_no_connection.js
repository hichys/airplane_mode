// $(document).ready(function () {
// 	// Override connection check
// 	frappe.ui.check_connection = function () {
// 		return true; // always online
// 	};
//
// 	// Disable offline event
// 	window.addEventListener("offline", function (e) {
// 		e.stopImmediatePropagation();
// 	});
//
// 	window.addEventListener("online", function (e) {
// 		e.stopImmediatePropagation();
// 	});
// });
// // 1. Force the property to always be true
Object.defineProperty(navigator, "onLine", { get: () => true });

// 2. Kill the 'offline' event so Frappe never hears it
window.addEventListener(
	"offline",
	(e) => {
		e.stopImmediatePropagation();
	},
	true,
);

// 3. (Optional) If Frappe already showed the message, hide it manually
$('.msgprint:contains("No Connection")').remove();
