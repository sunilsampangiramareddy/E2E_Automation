import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://www.google.com/?gws_rd=ssl&zx=1765283268971&no_sw_cr=1")
    page.get_by_role("combobox", name="Search").click()
    page.get_by_role("combobox", name="Search").fill("guru 99 selenium automation")
    page.goto("https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3Dguru%2B99%2Bselenium%2Bautomation%26sca_esv%3D8ff73cc9fbbf5111%26source%3Dhp%26ei%3DwhU4aczjLNyn5OUP--3C6QE%26iflsig%3DAOw8s4IAAAAAaTgj0uRDODAz1wUm2mehwO_v0RDsSH9d%26ved%3D0ahUKEwjMzKrQwLCRAxXcE7kGHfu2MB0Q4dUDCBA%26uact%3D5%26oq%3Dguru%2B99%2Bselenium%2Bautomation%26gs_lp%3DEgdnd3Mtd2l6IhtndXJ1IDk5IHNlbGVuaXVtIGF1dG9tYXRpb24yBhAAGBYYHjIGEAAYFhgeMgYQABgWGB4yBhAAGBYYHjIIEAAYCBgNGB4yCBAAGAgYDRgeMgsQABiABBiGAxiKBTILEAAYgAQYhgMYigUyCxAAGIAEGIYDGIoFMgUQABjvBUiweFDfFFjCbXACeACQAQOYAf8DoAGRLaoBDDEuMTUuNi40LjAuMbgBA8gBAPgBAZgCGqACwSaoAgrCAgoQABgDGOoCGI8BwgILEAAYgAQYsQMYgwHCAhEQLhiABBixAxjRAxiDARjHAcICCBAAGIAEGLEDwgIIEC4YgAQYsQPCAgUQABiABMICFBAuGIAEGLEDGMcBGJgFGJoFGK8BwgILEC4YgAQYsQMYgwHCAg4QLhiABBixAxjHARivAcICCxAAGIAEGLEDGMkDwgILEAAYgAQYkgMYigXCAgUQLhiABMICCxAuGIAEGMcBGK8BwgIHEAAYgAQYCsICAhAmwgIIEAAYFhgKGB7CAgkQABiABBgKGAvCAgcQIRigARgKwgIHEAAYgAQYDcICBhAAGA0YHsICCBAAGKIEGIkFwgIIEAAYgAQYogSYAxTxBY0Itxm5YNfXkgcKMi4xNS42LjIuMaAHmP0BsgcKMC4xNS42LjIuMbgHoSbCBwcyLTEyLjE0yAfgAYAIAA%26sclient%3Dgws-wiz%26sei%3D5hU4adzaE6auseMPipLjgQc&q=EgTKA3kEGOar4MkGIjCAFsoKFbdoZ_oUr0mOzt4O2WUJEN-m2CzpVt5w3Q94E47iTiQ1iw1B1bDfxmGbJmgyAVJaAUM")
    page.get_by_role("link", name="Selenium", exact=True).click()
    page.get_by_role("link", name="Home").click()
    page.locator("#inner-wrap").click()
    page.get_by_text("Simple & Easy Learning").click()
    page.locator(".cb-close").click()
    expect(page.get_by_role("link", name="Home")).to_be_visible()
    expect(page.locator("#menu-item-3172")).to_contain_text("Page")
