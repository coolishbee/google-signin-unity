# 유니티용 구글 로그인

안드로이드, iOS, 유니티 편집기 및 데스크톱 플레이어를 위한 구글 로그인 패키지입니다. 구글의 원본 저장소를 포크했으며, 참고 소스를 프로젝트의 목적에 맞게 재해석하고 수정했습니다.

안드로이드는 `CredentialManager`와 `AuthorizationClient`, iOS는 `GIDSignIn`을 사용합니다. 유니티 편집기와 데스크톱 플레이어는 로컬 콜백 수신기를 사용하는 브라우저 인증 방식으로 동작합니다. 네이티브 코드는 소스로 포함되며, 패키지를 사용하는 프로젝트를 빌드할 때 컴파일됩니다.

## 저장소 구조와 버전

저장소 루트는 유니티 프로젝트가 아닙니다.

| 경로 | 용도 |
|---|---|
| [패키지](../Packages/com.coolishbee.google-signin/) | 배포 가능한 유니티 패키지 |
| [예제 프로젝트](../SampleProject/) | 상대 경로로 패키지를 참조하는 예제 프로젝트 |

패키지 식별자는 `com.coolishbee.google-signin`, 버전은 `1.0.0`입니다. 런타임 어셈블리는 `GoogleSignIn`, 편집기 어셈블리는 `GoogleSignIn.Editor`이며, C# 네임스페이스는 `Google`입니다.

패키지에 명시된 최소 유니티 버전은 `2021.3`이며, 예제 프로젝트는 `6000.3.18f1`을 대상으로 합니다. 이번 패키지 재구성 과정에서는 유니티 편집기 실행, 컴파일, 빌드 및 기기 테스트를 수행하지 않았습니다.

## 로컬 설치

저장소의 `SampleProject/`를 열면 다음 상대 경로로 패키지를 참조합니다. 예제가 이미 포함되어 있으므로 다시 가져오면 클래스가 중복됩니다.

```json
"com.coolishbee.google-signin": "file:../../Packages/com.coolishbee.google-signin"
```

다른 프로젝트에서는 유니티 패키지 관리자에서 로컬의 `Packages/com.coolishbee.google-signin/package.json`을 선택하고 아래 의존성 레지스트리를 설정하세요. 예제를 가져오는 프로젝트에는 `com.unity.ugui`도 필요합니다.

## 공개 후 설치 예정 방법

다음 예시는 `upm/v1.0.0` 태그를 공개한 후 사용할 수 있습니다. 원격 배포, 릴리스 태그 공개 및 오픈유피엠 등록은 아직 완료되지 않았습니다.

```json
{
  "dependencies": {
    "com.coolishbee.google-signin": "https://github.com/coolishbee/google-signin-unity.git?path=Packages/com.coolishbee.google-signin#upm/v1.0.0"
  },
  "scopedRegistries": [
    {
      "name": "package.openupm.com",
      "url": "https://package.openupm.com",
      "scopes": ["com.coolishbee.google-signin", "com.google.external-dependency-manager"]
    }
  ]
}
```

오픈유피엠 등록과 배포가 완료되면 패키지 의존성 값을 `"1.0.0"`으로 변경할 수 있습니다. 기존 프로젝트 설정에 위 항목을 병합하세요. `com.google.external-dependency-manager`는 위 레지스트리에서, `com.unity.nuget.newtonsoft-json`은 유니티 레지스트리에서 가져옵니다.

## 이전 패키지에서 전환

새 패키지 식별자를 추가하기 전에 기존 `com.google.signin` 또는 `com.robbie111.google-signin` 의존성을 제거하세요. 클래스와 네이티브 코드의 중복을 방지하려면 `Assets/`에 가져온 이전 플러그인도 제거해야 합니다.

| 이전 어셈블리 참조 | 새 어셈블리 참조 |
|---|---|
| `GoogleSignin` 또는 `Robbie111.GoogleSignIn` | `GoogleSignIn` |
| `Robbie111.GoogleSignIn.Editor` | `GoogleSignIn.Editor` |

네임스페이스는 `Google`로 유지됩니다. 로그인 진입점은 구형 플러그인과 다릅니다.

- `SignInLegacy()`는 사용자 상호작용을 통한 로그인을 시작합니다. 안드로이드에서는 계정 선택 흐름을 요청합니다.
- `SignIn()`은 기존 계정을 우선 사용합니다. iOS에서는 이전 로그인을 복원하고, 편집기에서는 세션 캐시를 사용합니다. 독립 실행형 플레이어에서는 구현되어 있지 않습니다.
- 구형 `SignIn()`의 상호작용을 유지하려면 `SignInLegacy()`로 변경하세요. 구형 `SignInSilently()` 호출은 `SignIn()`으로 변경하세요. 관련 `Async` 및 `Future` 메서드에도 같은 이름 변경이 적용됩니다.
- 안드로이드의 `SignIn()`은 화면을 표시할 수 있으므로 항상 사용자 상호작용 없이 실행된다고 가정하지 마세요.

예제의 `OnSignInSilently`는 장면에 연결된 이벤트 메서드 이름이며, 내부적으로 현재의 `SignIn()`을 호출합니다.

## 설정 및 사용

인증 프로젝트에 플랫폼별 클라이언트를 등록하고 웹 클라이언트 식별자를 설정하세요. 안드로이드에서도 `WebClientId`에는 안드로이드 클라이언트 식별자가 아닌 웹 클라이언트 식별자가 필요합니다.

```csharp
using Google;

GoogleSignIn.Configuration = new GoogleSignInConfiguration {
    RequestEmail = true,
    RequestProfile = true,
    RequestIdToken = true,
    RequestAuthCode = true,
    WebClientId = "YOUR_WEB_CLIENT_ID.apps.googleusercontent.com",
#if UNITY_EDITOR || UNITY_STANDALONE
    ClientSecret = "YOUR_CLIENT_SECRET",
#endif
};

GoogleSignInUser user = await GoogleSignIn.DefaultInstance.SignInLegacy();
```

반환된 `IdToken`은 인증 연동에, `AuthCode`는 서버 측 인증 코드 교환에 사용하세요. 실제 인증 정보는 저장소에 커밋하지 마세요.

새 프로젝트에서는 패키지 관리자를 통해 제공된 예제를 가져오고, `Scenes/SampleScene.unity`를 연 뒤 예제 컴포넌트의 웹 클라이언트 식별자를 설정하세요. 저장소의 예제 장면은 [여기](../SampleProject/Assets/SignInSample/Scenes/SampleScene.unity)에 있습니다.

### 안드로이드 설정

앱의 패키지 이름과 서명 인증서 지문을 인증 콘솔에 등록한 값과 일치시키세요. 외부 의존성 관리 도구로 [의존성 선언 파일](../Packages/com.coolishbee.google-signin/Editor/GoogleSignInDependencies.xml)에 지정된 라이브러리를 가져오세요. 현재 구현은 구형 계정 이름 힌트와 게임 프로필 로그인을 지원하는 것으로 간주하면 안 됩니다.

### iOS 설정

인증 콘솔에서 내려받은 `.plist`를 프로젝트에 추가하세요. `BUNDLE_ID`는 프로젝트의 번들 식별자와 일치해야 합니다. `CLIENT_ID`와 `REVERSED_CLIENT_ID`는 필수이며, 서버 인증 코드가 필요하면 `WEB_CLIENT_ID`를 추가하세요.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>BUNDLE_ID</key>
    <string>com.yourcompany.yourapp</string>
    <key>CLIENT_ID</key>
    <string>YOUR_IOS_CLIENT_ID.apps.googleusercontent.com</string>
    <key>REVERSED_CLIENT_ID</key>
    <string>com.googleusercontent.apps.YOUR_IOS_CLIENT_ID</string>
    <key>WEB_CLIENT_ID</key>
    <string>YOUR_WEB_CLIENT_ID.apps.googleusercontent.com</string>
</dict>
</plist>
```

빌드 후처리는 이 값을 사용해 `Info.plist`의 `GIDClientID`, 콜백 주소 체계 및 선택적인 `GIDServerClientID`를 설정합니다. 의존성 파일에는 네이티브 패키지 `9.0.0`에 대한 스위프트 패키지 관리자 선언과 대체 가능한 코코아팟 선언이 포함되어 있습니다.

### 편집기 및 독립 실행형 플레이어의 제약

편집기의 재생 모드에서는 모바일 빌드 대상을 선택했더라도 데스크톱 인증 구현을 사용합니다. 모바일 네이티브 경로를 확인하려면 별도의 기기 빌드가 필요합니다.

현재 구현에는 토큰 갱신, `PKCE`, `state` 검증이 포함되어 있지 않습니다. 데스크톱 인증 흐름에는 추가 권한 범위가 적용되지 않습니다. 편집기 캐시는 프로세스가 종료되면 사라집니다. 편집기 및 독립 실행형 구현에는 `Disconnect()`와 `EnableDebugLogging()`이 구현되어 있지 않으며, 독립 실행형 플레이어에는 `SignIn()`도 구현되어 있지 않습니다.

## 인증 서비스 연동

`RequestIdToken = true`로 설정하고 반환된 `IdToken`으로 인증 서비스의 자격 증명을 생성하세요. 예를 들어 `Firebase.Auth.GoogleAuthProvider.GetCredential(user.IdToken, null)`의 결과를 `SignInWithCredentialAsync()`에 전달할 수 있습니다. 인증 서비스 패키지는 별도로 설치하고 설정해야 합니다.

## 원본 및 라이선스

이 프로젝트는 [구글의 원본 저장소](https://github.com/googlesamples/google-signin-unity)를 포크했습니다. 실제 구현은 [참고 저장소](https://github.com/Thaina/google-signin-unity)의 소스를 참고하여 프로젝트의 목적에 맞게 재해석하고 수정했습니다.

iOS 관련 기여에는 [관련 포크](https://github.com/pillsgood/google-signin-unity)와 [최초 기여](https://github.com/googlesamples/google-signin-unity/pull/205#issuecomment-1724733615)의 작업이 포함되어 있습니다. 기존 저작권 고지와 아파치 라이선스 2.0 전문은 소스 파일과 [라이선스 파일](../Packages/com.coolishbee.google-signin/LICENSE)에 보존되어 있습니다.
