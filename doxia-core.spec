Name:		doxia-core
Version:	2.0.0
Release:	1
Summary:	Doxia core classes
Group:		Development/Java
License:	ASL 2.0
URL:		https://maven.apache.org/doxia/doxia/
Source0:	https://github.com/apache/maven-doxia/archive/refs/tags/doxia-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python
BuildRequires:	mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:	mvn(commons-io:commons-io)
BuildRequires:	mvn(org.apache.commons:commons-text)
BuildRequires:	mvn(org.apache.commons:commons-lang3)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Doxia parses source documents into a sink. The XML pull parser
classes live in plexus-utils, so this build does not use plexus-xml.
Commons Text 1.15 provides the StringEscapeUtils methods HtmlTools calls.

%prep
%autosetup -n maven-doxia-doxia-%{version}
# The tag is the Doxia reactor. This package is only the core module.
# Its parent POM is that reactor, which is not packaged.
rm -rf src
mv doxia-core/src src
python - <<'PY'
import xml.etree.ElementTree as ET
NS = "http://maven.apache.org/POM/4.0.0"
ET.register_namespace("", NS)

def tag(name):
    return "{" + NS + "}" + name

def add(parent, name, text):
    node = ET.SubElement(parent, tag(name))
    node.text = text
    return node

root = ET.Element(tag("project"))
add(root, "modelVersion", "4.0.0")
add(root, "groupId", "org.apache.maven.doxia")
add(root, "artifactId", "doxia-core")
add(root, "version", "%{version}")
add(root, "name", "Doxia :: Core")
deps = ET.SubElement(root, tag("dependencies"))
for group, artifact, version in (
    ("org.apache.maven.doxia", "doxia-sink-api", "%{version}"),
    ("org.slf4j", "slf4j-api", "1.7.36"),
    ("javax.inject", "javax.inject", "1"),
    ("org.codehaus.plexus", "plexus-utils", "3.6.0"),
    ("commons-io", "commons-io", "2.22.0"),
    ("org.apache.commons", "commons-text", "1.15.0"),
    ("org.apache.commons", "commons-lang3", "3.21.0"),
):
    dep = ET.SubElement(deps, tag("dependency"))
    add(dep, "groupId", group)
    add(dep, "artifactId", artifact)
    add(dep, "version", version)
ET.ElementTree(root).write("pom.xml", encoding="utf-8", xml_declaration=True)
PY
rm -rf doxia-core doxia-modules doxia-sink-api doxia-test-docs

%files -f .mfiles
%doc README.md
