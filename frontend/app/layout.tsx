import type {Metadata} from "next";
import "./globals.css";
export const metadata:Metadata={title:"BhoomiDrishti | Land Acquisition Early Warning",description:"Predictive decision support for land-acquisition projects.",icons:{icon:"/favicon.svg",shortcut:"/favicon.svg"}};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
