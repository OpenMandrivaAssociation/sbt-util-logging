Name:		sbt-util-logging
Version:	1.11.5
Release:	2
Summary:	sbt logging classes used by Zinc
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/sbt/sbt
Source0:	sbt-util-logging-%{version}.tar.gz
# JLine 3.30.17 added a protected boolean field named closed.
Patch0:		sbt-util-logging-jline-closed.patch

BuildArch:	noarch
BuildRequires:	scala = 2.13.16
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	sysjar
BuildRequires:	sjson-new-core = 0.10.1
BuildRequires:	sjson-new-scalajson = 0.10.1
BuildRequires:	shaded-scalajson = 1.0.0.M4
BuildRequires:	shaded-jawn-parser = 1.3.2
BuildRequires:	sbt-io = 1.10.5
BuildRequires:	sbt-appmacro = 1.11.5
BuildRequires:	sbt-util = 1.11.5
BuildRequires:	mvn(org.scala-sbt:util-interface) = 1.11.5
BuildRequires:	mvn(org.scala-sbt:compiler-interface) = 1.12.0
BuildRequires:	mvn(org.scala-sbt.jline:jline) = 2.14.7.sbt
BuildRequires:	mvn(org.fusesource.jansi:jansi) = 2.4.3
BuildRequires:	mvn(org.jline:jline-terminal) = 3.30.17
BuildRequires:	mvn(org.jline:jline-native) = 3.30.17
BuildRequires:	mvn(org.apache.logging.log4j:log4j-api) = 2.26.1
BuildRequires:	mvn(org.apache.logging.log4j:log4j-core) = 2.26.1
BuildRequires:	mvn(com.swoval:file-tree-views) = 2.1.12
Requires:	mvn(org.scala-lang:scala-library) = 2.13.16
Requires:	mvn(org.scala-lang:scala-reflect) = 2.13.16
Requires:	mvn(com.eed3si9n:sjson-new-core_2.13) = 0.10.1
Requires:	mvn(com.eed3si9n:sjson-new-scalajson_2.13) = 0.10.1
Requires:	mvn(com.eed3si9n:shaded-scalajson_2.13) = 1.0.0.M4
Requires:	mvn(org.scala-sbt:io_2.13) = 1.10.5
Requires:	sbt-appmacro = 1.11.5
Requires:	sbt-util = 1.11.5
Requires:	mvn(org.scala-sbt:util-interface) = 1.11.5
Requires:	mvn(org.scala-sbt:compiler-interface) = 1.12.0
Requires:	mvn(org.scala-sbt.jline:jline) = 2.14.7.sbt
Requires:	mvn(org.fusesource.jansi:jansi) = 2.4.3
Requires:	mvn(org.jline:jline-terminal) = 3.30.17
Requires:	mvn(org.jline:jline-native) = 3.30.17
Requires:	mvn(org.apache.logging.log4j:log4j-api) = 2.26.1
Requires:	mvn(org.apache.logging.log4j:log4j-core) = 2.26.1

%description
sbt util-logging %{version} compiled for Scala 2.13.16. Zinc calls these
loggers. The checked-in contraband Scala sources are compiled with the
hand-written sources. Nothing is downloaded at build time.

%prep
%autosetup -n sbt-util-logging-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi
test -s LICENSE
test -s NOTICE
test -s compile.sh
test -s check.sh
test -s src/main/scala/sbt/util/Level.scala
test -s src/main/scala/sbt/internal/util/StringTypeTag.scala
test -s src/main/java/sbt/internal/util/DeprecatedJLine.java
grep -F -q 'implicit def fast' src/main/scala/sbt/internal/util/StringTypeTag.scala
grep -F -q 'import sbt.io.IO' src/main/scala/sbt/internal/util/StackTrace.scala

%build
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./compile.sh

%install
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
test -s sbt-util-logging.jar
cat > sbt-util-logging.pom << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.scala-sbt</groupId>
  <artifactId>util-logging_2.13</artifactId>
  <version>%{version}</version>
  <name>util-logging</name>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.scala-lang</groupId>
      <artifactId>scala-library</artifactId>
      <version>2.13.16</version>
    </dependency>
    <dependency>
      <groupId>org.scala-lang</groupId>
      <artifactId>scala-reflect</artifactId>
      <version>2.13.16</version>
    </dependency>
    <dependency>
      <groupId>com.eed3si9n</groupId>
      <artifactId>sjson-new-core_2.13</artifactId>
      <version>0.10.1</version>
    </dependency>
    <dependency>
      <groupId>com.eed3si9n</groupId>
      <artifactId>sjson-new-scalajson_2.13</artifactId>
      <version>0.10.1</version>
    </dependency>
    <dependency>
      <groupId>com.eed3si9n</groupId>
      <artifactId>shaded-scalajson_2.13</artifactId>
      <version>1.0.0.M4</version>
    </dependency>
    <dependency>
      <groupId>org.scala-sbt</groupId>
      <artifactId>io_2.13</artifactId>
      <version>1.10.5</version>
    </dependency>
    <dependency>
      <groupId>org.scala-sbt</groupId>
      <artifactId>util-interface</artifactId>
      <version>1.11.5</version>
    </dependency>
    <dependency>
      <groupId>org.scala-sbt</groupId>
      <artifactId>compiler-interface</artifactId>
      <version>1.12.0</version>
    </dependency>
    <dependency>
      <groupId>org.scala-sbt.jline</groupId>
      <artifactId>jline</artifactId>
      <version>2.14.7.sbt</version>
    </dependency>
    <dependency>
      <groupId>org.fusesource.jansi</groupId>
      <artifactId>jansi</artifactId>
      <version>2.4.3</version>
    </dependency>
    <dependency>
      <groupId>org.jline</groupId>
      <artifactId>jline-terminal</artifactId>
      <version>3.30.17</version>
    </dependency>
    <dependency>
      <groupId>org.jline</groupId>
      <artifactId>jline-native</artifactId>
      <version>3.30.17</version>
    </dependency>
    <dependency>
      <groupId>org.apache.logging.log4j</groupId>
      <artifactId>log4j-api</artifactId>
      <version>2.26.1</version>
    </dependency>
    <dependency>
      <groupId>org.apache.logging.log4j</groupId>
      <artifactId>log4j-core</artifactId>
      <version>2.26.1</version>
    </dependency>
  </dependencies>
</project>
EOF
mkdir -p %{buildroot}
sysjar install --buildroot %{buildroot} \
	--artifact sbt-util-logging.pom:sbt-util-logging.jar \
	--file-name util-logging-%{version} \
	--filelist .mfiles
test -s %{buildroot}%{_javadir}/util-logging-%{version}.jar
grep -F -q '"version": "%{version}"' %{buildroot}/usr/share/sysjar/index/org.scala-sbt/util-logging_2.13.sysjar

%check
set -eo pipefail
export JAVA_HOME=$(ls -d %{_jvmdir}/java-1.8.0-openjdk-* | head -n 1)
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
bash ./check.sh

%files -f .mfiles
%license LICENSE
%doc NOTICE
